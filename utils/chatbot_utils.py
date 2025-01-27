import re, requests, io
import google.generativeai as genai

from typing import Optional, Literal, Any
from pydantic import BaseModel

import configuration

from utils.line_related import LineBotHelper

line_bot_helper = LineBotHelper()
genai.configure(api_key=configuration.GEMINI_API_KEY)
descriptor_agent = genai.GenerativeModel("gemini-1.5-flash")


class TaskClassification(BaseModel):
    task_type: Literal["store_message", "respond_message", "tool_use"]


class MessageArgs(BaseModel):
    source: Literal["user", "group"]
    media_type: Literal["text", "image", "video", "audio", "file"]
    group_id: Optional[str]
    user_id: str
    profile_name: str
    task_classification: str
    should_respond: bool
    content: Any


def contains_aiko(message: str) -> bool:
    # Regex pattern to match variations of "Aiko" (case-insensitive, handles repeated letters)
    pattern = r"\b[aA]+[iI]+[kK]+[oO]+\b"
    return bool(re.search(pattern, message))


def process_response_to_get_content(response: requests.models.Response):
    binary_data = io.BytesIO(response.content)
    media_type = response.headers.get("Content-Type", "")
    myfile = genai.upload_file(binary_data, mime_type=media_type)
    id = myfile.name
    if media_type == "image/jpeg":
        result = descriptor_agent.generate_content([myfile, "\n\n", "Describe the image in detail"])
        description = result.text
    elif media_type == "application/pdf":
        


def get_message_args(event: dict) -> MessageArgs:
    source = line_bot_helper.get_message_source_type(event)
    media_type = line_bot_helper.get_message_type(event)
    group_id = line_bot_helper.get_group_id(event) if source == "group" else None
    user_id = line_bot_helper.get_user_id(event)
    profile_name = line_bot_helper.get_profile_name(event)

    should_respond = False
    if media_type == "text":
        message_text = line_bot_helper.get_message_text(event)
        if source == "group":
            should_respond = contains_aiko(message_text)  # Only respond if "Aiko" is mentioned
        elif source == "user":
            should_respond = True  # Alwyas respond to direct messages

    task_classification = "respond_message" if should_respond else "store_message"

    content = line_bot_helper.get_content(event)

    return MessageArgs(
        source=source,
        media_type=media_type,
        group_id=group_id,
        user_id=user_id,
        profile_name=profile_name,
        task_classification=task_classification,
        should_respond=should_respond,
        content=content,
    )


# TaskClassificationModel = LLMModel()
