import traceback
import os
import google.genai
import configuration
from utils.line_related import LineBotHelper
from utils import chatbot_utils, memory
from services.llm_models.model import LLMModel, ModelArgs

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

        chatbot_utils.update_memory(args, chat_histories, media_metadata, use_id)

        if args.should_respond:
            args.tool_name = client.models.generate_content(
                model="gemini-2.0-flash",
                contents="Determine whether and which tool is needed",
                config={"response_mime_type": "application/json", "response_schema": chatbot_utils.ToolsClassification},
            )
            if args.tool_name:
                message_data = None
                if args.tool_name == "waifu.it":  # Quote requests
                    reply_response = chatbot_utils.get_quote_from_waifuit()
                    message_data = {"messages": [{"type": "text", "text": reply_response}]}
                # elif args.tool_name == "trace.moe":  # Anime source search
                #     quoted_content = memory.get_quoted_content(args.quoted_message_id, use_id, chat_histories, media_metadata)
                #     reply_response = chatbot_utils.get_anime_info_from_tracemoe(quoted_content)
                LINEBOTHELPER.send_push_message(event=event, messages=message_data)
                memory.add_chat_history(
                    chat_histories=chat_histories,
                    chatroom_id=use_id,
                    message_id=args.message_id,
                    message=f"{configuration.BOT_CALL_NAME}: {reply_response}",
                )
                return
            prompt = chatbot_utils.generate_prompt(args, chat_histories, use_id, media_metadata)
            response_dict = MODEL.get_response(prompt)
            model_response = response_dict["content"]
            reply_response = LINEBOTHELPER.send_reply_message(event, model_response)
            chatbot_utils.update_histories(reply_response, chat_histories, model_responses, use_id, response_dict, model_response)

        chatbot_utils.sync_memory(chat_histories, model_responses, media_metadata, args)

    except Exception as e:
        print("Error processing event:", e)
        traceback.print_exc()
