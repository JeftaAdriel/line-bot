import os
import traceback

from dotenv import load_dotenv

import configuration

from utils.line_related import LineBotHelper
from utils import memory
from services.llm_models.model import LLMModel

load_dotenv()


def process_event(LINEBOTHELPER: LineBotHelper, MODEL: LLMModel, event: dict, chat_histories: dict, model_responses: dict):
    memory.add_chat_history(
        chat_histories=chat_histories,
        chatroom_id=LINEBOTHELPER.get_user_id(event),
        message=f"{LINEBOTHELPER.get_profile_name(event)}: {LINEBOTHELPER.get_message_text(event)}",
    )
    prompt = memory.get_chat_history(chat_histories=chat_histories, chatroom_id=LINEBOTHELPER.get_user_id(event))
    response_dict = MODEL.get_response(prompt)
    response = response_dict["content"]
    LINEBOTHELPER.send_reply_message(event, response)
    memory.add_chat_history(
        chat_histories=chat_histories, chatroom_id=LINEBOTHELPER.get_user_id(event), message=f"{configuration.BOT_NAME}: {response}"
    )
    memory.add_model_responses(model_responses, LINEBOTHELPER.get_user_id(event), response_dict)
    memory.sync_chat_histories_to_pantry(chat_histories=chat_histories)
    memory.sync_model_responses_to_pantry(model_responses=model_responses)
