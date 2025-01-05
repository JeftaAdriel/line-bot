from collections import deque
import configuration

chat_histories = {}
model_responses = {}


def add_chat_history(chatroom_id: str, message: str):
    if chatroom_id not in chat_histories:
        chat_histories[chatroom_id] = deque(maxlen=configuration.MAX_MESSAGE)
    chat_histories[chatroom_id].append(message)


def get_chat_history(chatroom_id: str) -> str:
    return "".join(f"{chat}\n" for chat in chat_histories[chatroom_id])


def get_all_chat_history():
    return chat_histories


def clear_chat_history(chatroom_id: str):
    chat_histories[chatroom_id].clear()


def add_model_responses(chatroom_id: str, response: dict):
    if chatroom_id not in model_responses:
        model_responses[chatroom_id] = []
    model_responses[chatroom_id].append(response)


def get_all_model_responses():
    return model_responses
