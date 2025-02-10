from collections import deque
from datetime import datetime, timezone
import io
import requests
import google.genai
import configuration
from utils import database_pantry

PANTRY_CHAT_HISTORY = "chat_histories"
PANTRY_MODEL_RESPONSES = "model_responses"
PANTRY_MEDIA_METADATA = "media_metadata"

client = google.genai.Client(api_key=configuration.GEMINI_API_KEY)


def sync_to_pantry(basket_name: str, data: dict):
    """Sync in data for the given basket name with Pantry."""
    database_pantry.store_data(basket_name, data)


def load_from_pantry(basket_name: str) -> dict:
    """Load data from the basket name in Pantry into memory."""
    return database_pantry.retrieve_data(basket_name)


def add_chat_history(chat_histories: dict, chatroom_id: str, message_id: str, message: str):
    if chatroom_id not in chat_histories:
        chat_histories[chatroom_id] = deque(maxlen=configuration.MAX_MESSAGE)
    chat_histories[chatroom_id].append({"message_id": message_id, "message": message})


def get_chat_history(chat_histories: dict, chatroom_id: str) -> str:
    entries = chat_histories.get(chatroom_id, [])
    messages = []
    for entry in entries:
        messages.append(entry["message"])
    return "\n".join(messages)


def clear_chat_history(chat_histories: dict, chatroom_id: str):
    chat_histories[chatroom_id].clear()


def add_model_responses(model_responses, chatroom_id: str, response: dict):
    if chatroom_id not in model_responses:
        model_responses[chatroom_id] = []
    model_responses[chatroom_id].append(response)


def add_media_metadata(media_metadata: dict, chatroom_id: str, message_id: str, file: google.genai.types.File):
    if chatroom_id not in media_metadata:
        media_metadata[chatroom_id] = []
    media_metadata[chatroom_id].append({"filename": file.name, "expiration_time": file.expiration_time.isoformat(), "message_id": message_id})


def clear_expired_media_metadata(media_metadata: dict, chatroom_id: str):
    if chatroom_id not in media_metadata:
        return
    now = datetime.now(timezone.utc)
    media_metadata[chatroom_id] = [entry for entry in media_metadata[chatroom_id] if datetime.fromisoformat(entry["expiration_time"]) > now]


def store_media_to_gemini_file(response: requests.models.Response):
    media_data = io.BytesIO(response.content)
    content_type = response.headers.get("Content-Type", "")
    myfile = client.files.upload(file=media_data, config={"mime_type": content_type})
    return myfile


def get_quoted_filename(media_metadata: dict, quoted_message_id: str, chatroom_id: str):
    filename = None
    if chatroom_id not in media_metadata:
        return None
    for entry in media_metadata[chatroom_id]:
        if entry["message_id"] == quoted_message_id:
            filename = entry["filename"]

    return filename


def get_quoted_text(chat_histories: dict, quoted_message_id: str, chatroom_id: str):
    quoted_text = None
    if chatroom_id not in chat_histories:
        return None
    for entry in chat_histories[chatroom_id]:
        if entry["message_id"] == quoted_message_id:
            quoted_text = entry["message"]

    return quoted_text


def get_quoted_content(quoted_message_id: str, use_id: str, chat_histories: dict, media_metadata: dict) -> str:
    filename = get_quoted_filename(media_metadata=media_metadata, quoted_message_id=quoted_message_id, chatroom_id=use_id)
    if filename is None:
        quoted_content = get_quoted_text(chat_histories=chat_histories, quoted_message_id=quoted_message_id, chatroom_id=use_id)
    else:
        quoted_content = client.files.get(name=filename)
    return quoted_content
