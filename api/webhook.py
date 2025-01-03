import os
import fastapi
import traceback
import time
import logging

from dotenv import load_dotenv
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration

# from utils.signature_validation import verify_signature


# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()
print("Sudah di sini 1")
configuration = Configuration(access_token=os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
print("Sudah di sini 2")
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))
print("Sudah di sini 3")

app = fastapi.FastAPI()
print("Sudah di sini 4")


@app.post("/webhook")
async def webhook(request):
    print(f"Received request: {request}")
    signature = request.headers.get("X-Line-Signature", "")
    r_body = await request.body()
    body_str = r_body.decode("utf-8")

    print(f"body_str: {body_str}")
    print(f"signature: {signature}")

    try:
        handler.handle(body_str, signature)
    except InvalidSignatureError as exc:
        raise fastapi.HTTPException(status_code=400, detail="Invalid signature. Please check your channel access token/channel secret.") from exc

    # is_valid = verify_signature(body_str, signature)
    # print(f"is_valid: {is_valid}")

    # print(f"Headers: {headers}")
    # print(f"Body: {body}")
    # body_json = await request.json()
    # x_line_signature = request.headers.get("x-line-signature")

    # is_valid = verify_signature(body, x_line_signature)

    # # Log the received event (incoming JSON)
    # logging.info("Received event: %s", body_json)

    # print(f"Headers: {headers}")
    # print(f"Received event: {body_json}")
    # print(f"Is Valid: {is_valid}")

    # Respond to acknowledge the request
    return {"status": "ok"}
