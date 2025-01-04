import os
import traceback
import time
import logging
import fastapi

from dotenv import load_dotenv

from utils import line_related

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
        body_str = r_body.decode("utf-8")

        # signature validation
        if not line_related.verify_signature(body_str, signature):
            raise fastapi.HTTPException(status_code=400, detail="Invalid signature. Please check your channel access token/channel secret.")

        events = r_body_json.get("events", [])

        # processing text messages for now
        msg_events = [event for event in events if event.get("message", {}).get("type") == "text"]
        for event in msg_events:
            reply_token = event.get("replyToken")
            print(f"reply_token: {reply_token}")
            line_related.send_message(reply_token)

        print(f"Body: {r_body}")
        print(f"Headers: {request.headers}")
        return fastapi.responses.JSONResponse(content={"message": "OK"})
    except Exception as e:
        print(f"Error processing webhook: {e}")
        traceback.print_exc()
        raise fastapi.HTTPException(status_code=500, detail="Internal server error")
