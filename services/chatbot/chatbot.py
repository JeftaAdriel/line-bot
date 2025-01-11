import os
import traceback
import re

from dotenv import load_dotenv

import configuration

from utils.line_related import LineBotHelper
from utils import memory
from services.llm_models.model import LLMModel

load_dotenv()


def contains_aiko(message: str) -> bool:
    # Regex pattern to match variations of "Aiko" (case-insensitive, handles repeated letters)
    pattern = r"\b[aA]+[iI]+[kK]+[oO]+\b"
    return bool(re.search(pattern, message))


def process_event(LINEBOTHELPER: LineBotHelper, MODEL: LLMModel, event: dict, chat_histories: dict, model_responses: dict):
    try:
        # Get basic information from event
        source = LINEBOTHELPER.get_message_source_type(event)
        message_text = LINEBOTHELPER.get_message_text(event)

        # Determine the ID to use based on source
        if source == "user":
            use_id = LINEBOTHELPER.get_user_id(event)
            should_respond = True  # Always respond to direct messages
        elif source == "group":
            use_id = LINEBOTHELPER.get_group_id(event)
            should_respond = contains_aiko(message_text)  # Only respond if "Aiko" is mentioned
        else:
            raise ValueError("Source type is neither user nor group")

        # Add message to chat history
        profile_name = LINEBOTHELPER.get_profile_name(event)
        memory.add_chat_history(
            chat_histories=chat_histories,
            chatroom_id=use_id,
            message=f"{profile_name}: {message_text}",
        )

        # Only get model response and reply if conditions are met
        if should_respond:
            # Get chat history and model response
            prompt = memory.get_chat_history(chat_histories=chat_histories, chatroom_id=use_id)
            response_dict = MODEL.get_response(prompt)
            response = response_dict["content"]

            # Send reply and update histories
            LINEBOTHELPER.send_reply_message(event, response)
            memory.add_chat_history(chat_histories=chat_histories, chatroom_id=use_id, message=f"{configuration.BOT_CALL_NAME}: {response}")
            memory.add_model_responses(model_responses, use_id, response_dict)

        # Sync histories regardless of whether we responded
        memory.sync_chat_histories_to_pantry(chat_histories=chat_histories)
        memory.sync_model_responses_to_pantry(model_responses=model_responses)

    except Exception as e:
        print("Error processing event:", e)
        traceback.print_exc()
