import os
import traceback
import time
import logging
import fastapi

from dotenv import load_dotenv

from utils.line_related import LineBotHelper
from utils.memory import Memory

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
load_dotenv()

app = fastapi.FastAPI()
LineBotHelper = LineBotHelper()
Memory = Memory()


@app.post("/webhook")
async def webhook(request: fastapi.Request):
    try:
        signature = request.headers.get("X-Line-Signature", "")
        r_body = await request.body()
        r_body_json = await request.json()
        body_str = r_body.decode("utf-8")

        # signature validation
        if not LineBotHelper.verify_signature(body_str, signature):
            raise fastapi.HTTPException(status_code=400, detail="Invalid signature. Please check your channel access token/channel secret.")

        events = r_body_json.get("events", [])

        # processing text messages for now
        msg_events = [event for event in events if event.get("message", {}).get("type", "") == "text"]
        for event in msg_events:
            Memory.add_chat_history(
                LineBotHelper.get_user_id(event), f"{LineBotHelper.get_profile_name(event)}: {LineBotHelper.get_message_text(event)}"
            )
            LineBotHelper.send_reply_message(event)

        print(f"Body: {r_body}")
        print(f"Headers: {request.headers}")
        print(f"Memory: {Memory.get_chat_history(LineBotHelper.get_group_id(event))}")
        return fastapi.responses.JSONResponse(content={"message": "OK"})
    except Exception as e:
        print(f"Error processing webhook: {e}")
        traceback.print_exc()
        raise fastapi.HTTPException(status_code=500, detail="Internal server error")
