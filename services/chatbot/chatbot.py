import traceback
import configuration

from utils.line_related import LineBotHelper
from utils import memory, chatbot_utils
from services.llm_models.model import LLMModel, ModelArgs

model_args = ModelArgs(framework=configuration.FRAMEWORK, provider=configuration.PROVIDER, system_prompt=configuration.SYSTEM_PROMPT)

LINEBOTHELPER = LineBotHelper()
MODEL = LLMModel(model_args=model_args)


def handle_events(events: list[dict], chat_histories: dict, model_responses: dict):
    for event in events:
        LINEBOTHELPER.display_loading_animation(event)
        message_args = chatbot_utils.get_message_args(event)
        process_event(message_args, event, chat_histories, model_responses)


def process_event(args: chatbot_utils.MessageArgs, event: dict, chat_histories: dict, model_responses: dict):
    try:
        # Determine the ID to use based on source
        if args.source == "user":
            use_id = args.user_id
        elif args.source == "group":
            use_id = args.group_id
        else:
            raise ValueError("Source type is neither user nor group")

        # Get the content of the message
        content = ""
        if args.media_type == "text":
            content = LINEBOTHELPER.get_message_text(event)

        # Add message to chat history
        memory.add_chat_history(
            chat_histories=chat_histories,
            chatroom_id=use_id,
            message=f"{args.profile_name}: {content}",
        )

        # Only get model response and reply if conditions are met
        if args.should_respond:
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
