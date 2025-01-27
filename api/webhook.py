import os
import traceback
import logging
import fastapi

from utils.line_related import LineBotHelper
from utils import memory, database_pantry
from services.chatbot import chatbot

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = fastapi.FastAPI()
LINEBOTHELPER = LineBotHelper()

try:
    chat_histories = memory.load_chat_histories_from_pantry()
except ValueError as e:
    chat_histories = {}
    database_pantry.create_basket(basket_name=memory.PANTRY_CHAT_HISTORY)


try:
    model_responses = memory.load_model_responses_from_pantry()
except ValueError as e:
    model_responses = {}
    database_pantry.create_basket(basket_name=memory.PANTRY_MODEL_RESPONSES)


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
        msg_events = [event for event in events if event.get("type", "") == "message"]
        # msg_events = [event for event in events if event.get("message", {}).get("type", "") == "text"]
        try:
            chatbot.handle_events(msg_events, chat_histories, model_responses)
            # for event in msg_events:
            #     LINEBOTHELPER.display_loading_animation(event)
            #     chatbot.process_event(event, chat_histories, model_responses)
        except Exception as e:
            print(f"Error processing message: {e}")
            traceback.print_exc()
            raise fastapi.HTTPException(status_code=500, detail="Internal server error")

        print(f"Body: {r_body}")
        print(f"Headers: {request.headers}")
        print(f"Chat History: {chat_histories}")
        print(f"Model Responses: {model_responses}")
        return fastapi.responses.JSONResponse(content={"message": "OK"})
    except Exception as e:
        print(f"Error processing webhook: {e}")
        traceback.print_exc()
        raise fastapi.HTTPException(status_code=500, detail="Internal server error")
