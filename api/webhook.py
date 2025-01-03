import os
import traceback
import time
import logging

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
load_dotenv()

app = FastAPI()
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))


@app.post("/webhook")
async def webhook(request: Request):
    # Parse the request body as JSON
    body = await request.json()

    # Log the received event (incoming JSON)
    logging.info("Received event: %s", body)

    print("Received event: %s", body)

    print(f"Headers: {request.headers}")

    # Respond to acknowledge the request
    return {"status": "ok"}
