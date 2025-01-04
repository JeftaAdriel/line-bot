import os
import traceback
import time
import logging
import fastapi

from dotenv import load_dotenv

from utils.line_related import LineBotHelper
from utils.memory import Memory
from services.llm_models.model import LLMModel
from services.chatbot import chatbot

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
load_dotenv()

app = fastapi.FastAPI()
LINEBOTHELPER = LineBotHelper()
MEMORY = Memory()
MODEL = LLMModel()


@app.post("/webhook")
async def webhook(request: fastapi.Request):
    try:
        signature = request.headers.get("X-Line-Signature", "")
        r_body = await request.body()
        r_body_json = await request.json()
        body_str = r_body.decode("utf-8")

        # signature validation
        if not LINEBOTHELPER.verify_signature(body_str, signature):
            raise fastapi.HTTPException(status_code=400, detail="Invalid signature. Please check your channel access token/channel secret.")

        events = r_body_json.get("events", [])

        # processing text messages for now
        msg_events = [event for event in events if event.get("message", {}).get("type", "") == "text"]
        try:
            for event in msg_events:
                chatbot.process_event(MEMORY, LINEBOTHELPER, MODEL, event)
        except Exception as e:
            print(f"Error processing message: {e}")
            traceback.print_exc()
            raise fastapi.HTTPException(status_code=500, detail="Internal server error")

        print(f"Body: {r_body}")
        print(f"Headers: {request.headers}")
        print(f"Memory: {MEMORY.get_all_chat_history()}")
        return fastapi.responses.JSONResponse(content={"message": "OK"})
    except Exception as e:
        print(f"Error processing webhook: {e}")
        traceback.print_exc()
        raise fastapi.HTTPException(status_code=500, detail="Internal server error")
