import traceback
import os
import json
import google.genai
import configuration
from utils.line_related import LineBotHelper
from utils import memory, chatbot_utils
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
        # Determine the ID to use based on source
        if args.source == "user":
            use_id = args.user_id
        elif args.source == "group":
            use_id = args.group_id
        else:
            raise ValueError("Source type is neither user nor group")

        if args.content in configuration.template_keyword_responses:
            message_data = {"messages": [configuration.template_keyword_responses[args.content]]}
            if LINEBOTHELPER.validate_message(message_data):
                response = LINEBOTHELPER.send_push_message(event=event, messages=message_data)
                print(f"Sent response: {response}")
            return

        # Update memory
        if args.media_type == "text":
            message = f"{args.profile_name}: {args.content}"
        else:
            message = f"{args.profile_name} {args.content}"
        memory.add_chat_history(
            chat_histories=chat_histories,
            chatroom_id=use_id,
            message_id=args.message_id,
            message=message,
        )
        memory.clear_expired_media_metadata(media_metadata=media_metadata, chatroom_id=use_id)
        if args.myfile is not None:
            memory.add_media_metadata(media_metadata=media_metadata, chatroom_id=use_id, message_id=args.message_id, file=args.myfile)

        # Only get model response and reply if conditions are met
        if args.should_respond:

            if args.quoted_message_id is not None:
                quoted_content = memory.get_quoted_content(args.quoted_message_id, use_id, chat_histories, media_metadata)
                prompt = ["Konten yang dikutip: ", "\n", quoted_content, "\n\n", "Histori Percakapan: ", "\n", args.content]
            else:
                prompt = [memory.get_chat_history(chat_histories=chat_histories, chatroom_id=use_id)]

            print(f"Prompt: {prompt}")
            response_dict = MODEL.get_response(prompt)
            response = response_dict["content"]

            # Send reply and update histories
            reply_response = LINEBOTHELPER.send_reply_message(event, response)
            reply_response_data = json.loads(reply_response.content.decode("utf-8"))
            print(f"Reply response: {reply_response}")
            print(f"Reply Response Content: {reply_response.content}")
            print(f"Bot Response: {response}")
            message_ids = [message["id"] for message in reply_response_data.get("sentMessages", [])]
            for message_id in message_ids:
                memory.add_chat_history(
                    chat_histories=chat_histories, chatroom_id=use_id, message_id=message_id, message=f"{configuration.BOT_CALL_NAME}: {response}"
                )
            memory.add_model_responses(model_responses, use_id, response_dict)

        # Sync histories regardless of whether we responded
        memory.sync_to_pantry(basket_name=memory.PANTRY_CHAT_HISTORY, data=chat_histories)
        memory.sync_to_pantry(basket_name=memory.PANTRY_MODEL_RESPONSES, data=model_responses)
        if args.myfile is not None:
            memory.sync_to_pantry(basket_name=memory.PANTRY_MEDIA_METADATA, data=media_metadata)

    except Exception as e:
        print("Error processing event:", e)
        traceback.print_exc()
