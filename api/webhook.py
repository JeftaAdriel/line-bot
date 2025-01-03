import logging
from fastapi import FastAPI, Request

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()


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
