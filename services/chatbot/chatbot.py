import os
import traceback

from dotenv import load_dotenv

from utils.line_related import LineBotHelper
from utils import memory
from services.llm_models.model import LLMModel

load_dotenv()


def process_event(LINEBOTHELPER: LineBotHelper, MODEL: LLMModel, event: dict):
    memory.add_chat_history(
        chatroom_id=LINEBOTHELPER.get_user_id(event), message=f"{LINEBOTHELPER.get_profile_name(event)}: {LINEBOTHELPER.get_message_text(event)}"
    )
    prompt = memory.get_chat_history(LINEBOTHELPER.get_user_id(event))
    response_dict = MODEL.get_response(prompt)
    response = response_dict["content"]
    LINEBOTHELPER.send_reply_message(event, response)
