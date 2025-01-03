import os
import traceback
import time
import logging
import fastapi

from dotenv import load_dotenv
from linebot.v3.exceptions import InvalidSignatureError

from utils.signature_validation import verify_signature

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
load_dotenv()

app = fastapi.FastAPI()
print("sampai sini 1")


@app.post("/webhook")
async def webhook(request: fastapi.Request):
    print("sampai sini 2")
    signature = request.headers.get("X-Line-Signature", "")
    r_body = await request.body()
    body_str = r_body.decode("utf-8")
    if not verify_signature(body_str, signature):
        raise fastapi.HTTPException(status_code=400, detail="Invalid signature. Please check your channel access token/channel secret.")

    print("Received event: %s", r_body)
    print(f"Headers: {request.headers}")

    return fastapi.responses.JSONResponse(content={"message": "OK"})
