import re
import requests
import json
import google.genai
from typing import Optional, Literal, Any
from pydantic import BaseModel, Field
import configuration
from utils import memory
from utils.line_related import LineBotHelper

line_bot_helper = LineBotHelper()
client = google.genai.Client(api_key=configuration.GEMINI_API_KEY)


class TaskClassification(BaseModel):
    task_type: Literal["store_message", "respond_message", "tool_use"]


class ToolsClassification(BaseModel):
    tool_name: Literal["waifu.it", "trace.moe", None] = Field(
        description="The name of the tool to use for the user's request. 'waifu.it' for quote requests, 'trace.moe' for anime source search, None if no tool is needed."
    )


class MessageArgs(BaseModel):
    message_id: str
    source: Literal["user", "group"]
    media_type: Literal["text", "image", "video", "audio", "file"]
    group_id: Optional[str]
    user_id: str
    profile_name: str
    task_classification: str
    should_respond: bool
    content: Any
    myfile: Any
    quoted_message_id: Optional[str]
    tool_name: ToolsClassification


def contains_aiko(message: str) -> bool:
    """Regex pattern to match variations of "Aiko" (case-insensitive, handles repeated letters)"""
    pattern = r"\b[aA]+[iI]+[kK]+[oO]+\b"
    return bool(re.search(pattern, message))


def get_use_id(args: MessageArgs) -> str:
    if args.source == "user":
        return args.user_id
    elif args.source == "group":
        return args.group_id
    else:
        raise ValueError("Source type is neither user nor group")


def respond_to_template_keyword(args: MessageArgs, event: dict) -> bool:
    if args.content in configuration.template_keyword_responses:
        message_data = {"messages": [configuration.template_keyword_responses[args.content]]}
        if line_bot_helper.validate_message(message_data):
            line_bot_helper.send_push_message(event=event, messages=message_data)
        return True
    return False


def update_memory(args: MessageArgs, chat_histories: dict, media_metadata: dict, use_id: str):
    message = f"{args.profile_name}: {args.content}" if args.media_type == "text" else f"{args.profile_name} {args.content}"
    memory.add_chat_history(chat_histories=chat_histories, chatroom_id=use_id, message_id=args.message_id, message=message)
    memory.clear_expired_media_metadata(media_metadata=media_metadata, chatroom_id=use_id)
    if args.myfile:
        memory.add_media_metadata(media_metadata, use_id, args.message_id, args.myfile)


def generate_prompt(args: MessageArgs, chat_histories: dict, use_id: str, media_metadata: dict) -> list:
    if args.quoted_message_id:
        quoted_content = memory.get_quoted_content(args.quoted_message_id, use_id, chat_histories, media_metadata)
        prompt = ["Konten yang dikutip: ", "\n", quoted_content, "\n\n", "Histori Percakapan: ", "\n", args.content]
    else:
        prompt = [memory.get_chat_history(chat_histories=chat_histories, chatroom_id=use_id)]
    return prompt


def update_histories(reply_response, chat_histories: dict, model_responses: dict, use_id: str, response_dict: dict, model_response: str):
    reply_response_data = json.loads(reply_response.content.decode("utf-8"))
    message_ids = [message["id"] for message in reply_response_data.get("sentMessages", [])]
    for message_id in message_ids:
        memory.add_chat_history(
            chat_histories=chat_histories, chatroom_id=use_id, message_id=message_id, message=f"{configuration.BOT_CALL_NAME}: {model_response}"
        )
    memory.add_model_responses(model_responses, use_id, response_dict)


def sync_memory(chat_histories: dict, model_responses: dict, media_metadata: dict, args: MessageArgs):
    memory.sync_to_pantry(basket_name=memory.PANTRY_CHAT_HISTORY, data=chat_histories)
    memory.sync_to_pantry(basket_name=memory.PANTRY_MODEL_RESPONSES, data=model_responses)
    if args.myfile:
        memory.sync_to_pantry(basket_name=memory.PANTRY_MEDIA_METADATA, data=media_metadata)


def get_message_args(event: dict) -> MessageArgs:
    message_id = line_bot_helper.get_message_id(event)
    source = line_bot_helper.get_message_source_type(event)
    media_type = line_bot_helper.get_message_type(event)
    group_id = line_bot_helper.get_group_id(event) if source == "group" else None
    user_id = line_bot_helper.get_user_id(event)
    profile_name = line_bot_helper.get_profile_name(event)
    should_respond = False
    content, myfile = line_bot_helper.get_content_and_file(event)
    if media_type == "text":
        if source == "group":
            should_respond = contains_aiko(content)  # Only respond if "Aiko" is mentioned
        elif source == "user":
            should_respond = True  # Alwyas respond to direct messages

    task_classification = "respond_message" if should_respond else "store_message"

    if "quotedMessageId" in event["message"]:
        quoted_message_id = line_bot_helper.get_quoted_message_id(event)
    else:
        quoted_message_id = None

    tool_name = None

    return MessageArgs(
        message_id=message_id,
        source=source,
        media_type=media_type,
        group_id=group_id,
        user_id=user_id,
        profile_name=profile_name,
        task_classification=task_classification,
        should_respond=should_respond,
        content=content,
        myfile=myfile,
        quoted_message_id=quoted_message_id,
        tool_name=tool_name,
    )


def get_quote_from_waifuit() -> str:
    url = "https://waifu.it/api/v4/quote"
    response = requests.get(url, headers={"Authorization": configuration.WAIFUIT_TOKEN})
    data = response.json()
    text = f"{data['quote']}\n\n- {data['author']} from {data['anime']}"
    return text


# def get_anime_info_from_tracemoe(image_file: google.genai.types.File):


# TaskClassificationModel = LLMModel()
