import os
import traceback
import time
import logging
import fastapi

from dotenv import load_dotenv

from utils.signature_validation import verify_signature
from utils.send_messages import send_message

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
load_dotenv()

app = fastapi.FastAPI()


@app.post("/webhook")
async def webhook(request: fastapi.Request):
    try:
        signature = request.headers.get("X-Line-Signature", "")
        r_body = await request.body()
        r_body_json = await request.json()
        print(f"r_body_json: {r_body_json}")
        body_str = r_body.decode("utf-8")

        print(f"body_str_type: {type(body_str)}")
        print(f"signature_type: {type(signature)}")

        # signature validation
        if not verify_signature(body_str, signature):
            raise fastapi.HTTPException(status_code=400, detail="Invalid signature. Please check your channel access token/channel secret.")

        events = r_body_json.get("events", [])

        # processing text messages for now
        msg_events = [event for event in events if event.get("message", {}).get("type") == "text"]
        for event in msg_events:
            reply_token = event.get("replyToken")
            print(f"reply_token: {reply_token}")
            print(f"reply_token_type: {type(reply_token)}")
            send_message(reply_token)

        print(f"Received event: {r_body}")
        print(f"Headers: {request.headers}")
        return fastapi.responses.JSONResponse(content={"message": "OK"})
    except Exception as e:
        print(f"Error processing webhook: {e}")
        traceback.print_exc()
        raise fastapi.HTTPException(status_code=500, detail="Internal server error")
