import traceback
import os
import google.genai
import configuration
from utils.line_related import LineBotHelper
from utils import chatbot_utils
from services.llm_models.model import LLMModel
from services.llm_models.model import ModelArgs

client = google.genai.Client(api_key=os.environ["GEMINI_API_KEY"])
model_args = ModelArgs(framework=configuration.FRAMEWORK, provider=configuration.PROVIDER, system_prompt=configuration.SYSTEM_PROMPT)

LINEBOTHELPER = LineBotHelper()
MODEL = LLMModel(model_args=model_args)


def handle_events(events: list[dict], chat_histories: dict, model_responses: dict, media_metadata: dict):
    for event in events:
        LINEBOTHELPER.display_loading_animation(event)
        message_args = chatbot_utils.get_message_args(event)
        process_event(message_args, event, chat_histories, model_responses, media_metadata)


def process_event(args: chatbot_utils.MessageArgs, event: dict, chat_histories: dict, model_responses: dict, media_metadata: dict):
    try:
        use_id = chatbot_utils.get_use_id(args)
        if chatbot_utils.respond_to_template_keyword(args, event):
            return

        chatbot_utils.update_memory(args, event, chat_histories, media_metadata, use_id)

        if args.should_respond:
            prompt = chatbot_utils.generate_prompt(args, chat_histories, use_id, media_metadata)
            response_dict = MODEL.get_response(prompt)
            model_response = response_dict["content"]
            reply_response = LINEBOTHELPER.send_reply_message(event, model_response)
            chatbot_utils.update_histories(reply_response, chat_histories, model_responses, use_id, response_dict, model_response)

        chatbot_utils.sync_memory(chat_histories, model_responses, media_metadata, args)

    except Exception as e:
        print("Error processing event:", e)
        traceback.print_exc()
