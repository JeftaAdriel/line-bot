import logging
import fastapi
from utils import signature_validation

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = fastapi.FastAPI()


@app.post("/webhook")
async def webhook(request: fastapi.Request):
    headers = await request.headers
    body = await request.json()

    is_valid = signature_validation(request)

    # Log the received event (incoming JSON)
    logging.info("Received event: %s", body)

    print(f"Headers: {headers}")
    print(f"Received event: {body}")
    print(f"Is Valid: {is_valid}")

    # Respond to acknowledge the request
    return {"status": "ok"}
