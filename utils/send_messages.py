import os
import requests
from dotenv import load_dotenv

load_dotenv()

destination_url = "https://api.line.me/v2/bot/message/reply"
headers = {"Authorization": f'Bearer {os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")}', "Content-Type": "application/json"}
print(f"Send Headers: {headers}")


def send_message(reply_token):
    data = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": "Hi!"}],
    }

    response = requests.post(destination_url, headers=headers, json=data, timeout=10)
    print(f"Response: {response.status_code}, {response.text}")
    return response
