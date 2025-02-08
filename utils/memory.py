import google.generativeai as old_genai
from collections import deque
from datetime import datetime, timezone
import configuration
from utils import database_pantry

PANTRY_CHAT_HISTORY = "chat_histories"
PANTRY_MODEL_RESPONSES = "model_responses"
PANTRY_MEDIA_METADATA = "media_metadata"


def sync_to_pantry(basket_name: str, data: dict):
    """Sync in data for the given basket name with Pantry."""
    database_pantry.store_data(basket_name, data)


def load_from_pantry(basket_name: str) -> dict:
    """Load data from the basket name in Pantry into memory."""
    return database_pantry.retrieve_data(basket_name)


def add_chat_history(chat_histories: dict, chatroom_id: str, message: str):
    if chatroom_id not in chat_histories:
        chat_histories[chatroom_id] = deque(maxlen=configuration.MAX_MESSAGE)
    chat_histories[chatroom_id].append(message)


def get_chat_history(chat_histories: dict, chatroom_id: str) -> str:
    return "".join(f"{chat}\n" for chat in chat_histories.get(chatroom_id, []))


def clear_chat_history(chat_histories: dict, chatroom_id: str):
    chat_histories[chatroom_id].clear()


def add_model_responses(model_responses, chatroom_id: str, response: dict):
    if chatroom_id not in model_responses:
        model_responses[chatroom_id] = []
    model_responses[chatroom_id].append(response)


def add_media_metadata(media_metadata: dict, chatroom_id: str, message_id: str, file: old_genai.types.file_types.File):
    if chatroom_id not in media_metadata:
        media_metadata[chatroom_id] = []
    media_metadata[chatroom_id].append({"filename": file.name, "expiration_time": file.expiration_time, "message_id": message_id})


def clear_expired_media_metadata(media_metadata: dict, chatroom_id: str):
    if chatroom_id not in media_metadata:
        return
    now = datetime.now(timezone.utc)
    media_metadata[chatroom_id] = [entry for entry in media_metadata[chatroom_id] if entry["expiration_time"] > now]
