from collections import deque
import config


class Memory:
    def __init__(self):
        self.chat_histories = {}

    def add_chat_history(self, chatroom_id, message):
        if chatroom_id not in self.chat_histories:
            deque(maxlen=config.MAX_MESSAGE)
        self.chat_histories[chatroom_id].append(message)

    def get_chat_history(self, chatroom_id):
        return "".join(f"{chat}\n" for chat in self.chat_histories[chatroom_id])

    def clear_chat_history(self, chatroom_id):
        self.chat_histories[chatroom_id].clear()
