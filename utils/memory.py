from collections import deque
import configuration


class Memory:
    def __init__(self):
        self.chat_histories = {}
        self.model_responses = {}

    def add_chat_history(self, chatroom_id: str, message: str):
        if chatroom_id not in self.chat_histories:
            self.chat_histories[chatroom_id] = deque(maxlen=configuration.MAX_MESSAGE)
        self.chat_histories[chatroom_id].append(message)

    def get_chat_history(self, chatroom_id: str) -> str:
        return "".join(f"{chat}\n" for chat in self.chat_histories[chatroom_id])

    def get_all_chat_history(self):
        return self.chat_histories

    def clear_chat_history(self, chatroom_id: str):
        self.chat_histories[chatroom_id].clear()
