import traceback
import logging
import fastapi
from utils.line_related import LineBotHelper
from utils import memory
from services.chatbot import chatbot

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = fastapi.FastAPI()
LINEBOTHELPER = LineBotHelper()

try:
    chat_histories = memory.load_from_pantry(basket_name=memory.PANTRY_CHAT_HISTORY)
except ValueError:
    chat_histories = {}

try:
    model_responses = memory.load_from_pantry(basket_name=memory.PANTRY_MODEL_RESPONSES)
except ValueError:
    model_responses = {}

try:
    media_metadata = memory.load_from_pantry(basket_name=memory.PANTRY_MEDIA_METADATA)
except ValueError:
    media_metadata = {}


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
        try:
            chatbot.handle_events(msg_events, chat_histories, model_responses, media_metadata)
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
