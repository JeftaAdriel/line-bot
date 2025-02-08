import re
from typing import Optional, Literal, Any
from pydantic import BaseModel
from utils.line_related import LineBotHelper

line_bot_helper = LineBotHelper()


class TaskClassification(BaseModel):
    task_type: Literal["store_message", "respond_message", "tool_use"]


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


def contains_aiko(message: str) -> bool:
    # Regex pattern to match variations of "Aiko" (case-insensitive, handles repeated letters)
    pattern = r"\b[aA]+[iI]+[kK]+[oO]+\b"
    return bool(re.search(pattern, message))


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

    print(f"myfile Y: {myfile}")
    print(f"myfile type Y: {type(myfile)}")

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
    )


# TaskClassificationModel = LLMModel()
