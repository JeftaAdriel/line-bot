import base64
import hashlib
import hmac
import os
import requests
import logging

from configuration import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
from utils import chatbot_utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LINE_API_BASE_URL = "https://api.line.me/v2/bot"
LINE_API_DATA_URL = "https://api-data.line.me/v2/bot"
headers = {"Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}", "Content-Type": "application/json"}


class LineBotHelper:
    def __init__(self):
        self.headers = headers
        self.channel_secret = LINE_CHANNEL_SECRET
        self.access_token = LINE_CHANNEL_ACCESS_TOKEN

    # Validations
    def verify_signature(self, body: str, x_line_signature: str) -> bool:
        if not self.channel_secret:
            raise ValueError("LINE_CHANNEL_SECRET is not set in environment variables (and maybe configuration.py).")
        gen_signature = hmac.new(self.channel_secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256).digest()
        return hmac.compare_digest(x_line_signature.encode("utf-8"), base64.b64encode(gen_signature))

    # Informations
    def get_message_type(self, event: dict) -> str:
        return event["message"]["type"]

    def get_message_id(self, event: dict) -> str:
        return event["message"]["id"]

    def get_message_source_type(self, event: dict) -> str:
        return event["source"]["type"]

    def get_user_id(self, event: dict) -> str:
        return event["source"]["userId"]

    def get_group_id(self, event: dict) -> str:
        return event["source"]["groupId"]

    def get_profile(self, event: dict) -> dict:
        user_id = self.get_user_id(event)
        source_type = self.get_message_source_type(event)
        destination_url = None
        if source_type == "group":
            group_id = self.get_group_id(event)
            destination_url = f"{LINE_API_BASE_URL}/group/{group_id}/member/{user_id}"
        elif source_type == "user":
            destination_url = f"{LINE_API_BASE_URL}/profile/{user_id}"
        return requests.get(destination_url, headers=headers, timeout=10)

    def get_profile_name(self, event: dict) -> str:
        profile = self.get_profile(event)
        return profile.json()["displayName"]

    def get_message_text(self, event: dict) -> str:
        return event["message"]["text"]

    def get_content(self, event: dict):
        message_id = self.get_message_id(event)
        media_type = self.get_message_type(event)
        if media_type in ["text"]:
            return self.get_message_text(event)
        elif media_type in ["image", "video", "audio", "file"]:
            destination_url = f"{LINE_API_DATA_URL}/message/{message_id}/content"
            response = requests.get(destination_url, headers=headers, timeout=10)
            if response.status_code == 200:
                chatbot_utils.process_response_to_get_content(response)
            else:
                raise ValueError(f"Failed to get content from \n {event}")
            pass
        else:
            raise ValueError("Unsupported media type")

    # Actions
    def send_reply_message(self, event: dict, response: str):
        reply_token = event["replyToken"]
        destination_url = f"{LINE_API_BASE_URL}/message/reply"
        data = {
            "replyToken": reply_token,
            "messages": [{"type": "text", "text": f"{response}"}],
        }
        response = requests.post(destination_url, headers=headers, json=data, timeout=10)
        print(f"Response: {response.status_code}, {response.text}")
        return response

    def display_loading_animation(self, event: dict):
        user_id = self.get_user_id(event)
        destination_url = f"{LINE_API_BASE_URL}/chat/loading/start"
        response = requests.post(destination_url, headers=headers, json={"chatId": user_id, "loadingSeconds": 15}, timeout=10)
        return response
