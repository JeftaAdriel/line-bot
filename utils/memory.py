from collections import deque
import configuration
from utils import database_pantry

PANTRY_CHAT_HISTORY = "chat_histories"
PANTRY_MODEL_RESPONSES = "model_responses"


def sync_chat_histories_to_pantry(chat_histories: dict):
    """Sync in-memory chat histories with Pantry."""
    database_pantry.store_data(PANTRY_CHAT_HISTORY, chat_histories)


def load_chat_histories_from_pantry():
    """Load chat histories from Pantry into memory."""
    chat_histories = database_pantry.retrieve_data(PANTRY_CHAT_HISTORY)
    return chat_histories


def sync_model_responses_to_pantry(model_responses: dict):
    """Sync in-memory model responses with Pantry."""
    database_pantry.store_data(PANTRY_MODEL_RESPONSES, model_responses)


def load_model_responses_from_pantry():
    """Load model responses from Pantry into memory."""
    model_responses = database_pantry.retrieve_data(PANTRY_MODEL_RESPONSES)
    return model_responses


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
