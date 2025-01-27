from collections import deque
from datetime import datetime, timedelta
import configuration
from utils import database_pantry

PANTRY_CHAT_HISTORY = "chat_histories"
PANTRY_MODEL_RESPONSES = "model_responses"
PANTRY_MEDIA_METADATA = "media_metadata"


def sync_to_pantry(basket_name: str, data: dict):
    """Sync in data for the given basket name with Pantry."""
    try:
        database_pantry.store_data(basket_name, data)
    except ValueError:
        database_pantry.create_basket(basket_name)
        database_pantry.store_data(basket_name, data)


# def sync_chat_histories_to_pantry(chat_histories: dict):
#     """Sync in-memory chat histories with Pantry."""
#     database_pantry.store_data(PANTRY_CHAT_HISTORY, chat_histories)


def load_from_pantry(basket_name: str) -> dict:
    """Load data from the basket name in Pantry into memory."""
    try:
        return database_pantry.retrieve_data(basket_name)
    except ValueError:
        database_pantry.create_basket(basket_name)
        return {}


# def sync_model_responses_to_pantry(model_responses: dict):
#     """Sync in-memory model responses with Pantry."""
#     database_pantry.store_data(PANTRY_MODEL_RESPONSES, model_responses)


# def load_model_responses_from_pantry():
#     """Load model responses from Pantry into memory."""
#     model_responses = database_pantry.retrieve_data(PANTRY_MODEL_RESPONSES)
#     return model_responses


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


# def add_media_metadata(media_metadata: dict, media_id: str, chatroom_id: str, filename: str):
#     """Store media metadata with expiry time (48 hours from now)."""
#     upload_time = datetime.now()
#     expiry_time = upload_time + timedelta(hours=48)
#     if chatroom_id not in media_metadata:
#         media_metadata[chatroom_id] = {}
#     media_metadata[chatroom_id][media_id] = {
#         'expiry': expiry_time.isoformat(),
#         'filename': filename,
#         'upload_time': upload_time.isoformat()
#     }
#     sync_media_metadata_to_pantry(media_metadata)
