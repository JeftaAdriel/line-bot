import base64
import hashlib
import hmac
import os
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {"Authorization": f'Bearer {os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")}', "Content-Type": "application/json"}


def verify_signature(body: str, x_line_signature: str):
    channel_secret = os.environ.get("LINE_CHANNEL_SECRET")
    if not channel_secret:
        raise ValueError("LINE_CHANNEL_SECRET is not set in environment variables.")
    gen_signature = hmac.new(channel_secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256).digest()
    return hmac.compare_digest(x_line_signature.encode("utf-8"), base64.b64encode(gen_signature))


def send_message(reply_token: str):
    destination_url = "https://api.line.me/v2/bot/message/reply"
    data = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": "Hi!"}],
    }

    response = requests.post(destination_url, headers=headers, json=data, timeout=10)
    print(f"Response: {response.status_code}, {response.text}")
    return response


def get_message_id(event: dict) -> str:
    return event["message"]["id"]


def get_content(event: dict) -> str:
    """
    Get content for other than text messages
    """
    message_id = get_message_id(event)
    destination_url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
    return requests.get(destination_url, headers=headers, timeout=10)
