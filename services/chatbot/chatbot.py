import traceback
import google.generativeai as old_genai
import configuration
from utils.line_related import LineBotHelper
from utils import memory, chatbot_utils
from services.llm_models.model import LLMModel, ModelArgs

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

        print(f"myfile: {type(myfile)}")
        print(f"myfile type 3: {type(args.myfile)}")

        # Update memory
        memory.add_chat_history(
            chat_histories=chat_histories,
            chatroom_id=use_id,
            message=f"{args.profile_name}: {args.content}",
        )
        memory.clear_expired_media_metadata(media_metadata=media_metadata, chatroom_id=use_id)
        if args.myfile is not None:
            memory.add_media_metadata(media_metadata=media_metadata, chatroom_id=use_id, message_id=args.message_id, file=args.myfile)

        # Only get model response and reply if conditions are met
        if args.should_respond:

            if args.quoted_message_id is not None:
                filename = LINEBOTHELPER.get_filename(media_metadata=media_metadata, quoted_message_id=args.quoted_message_id, chatroom_id=use_id)
                if filename is not None:
                    myfile = old_genai.get_file(filename)
                    prompt = [myfile, args.content]
                else:
                    prompt = memory.get_chat_history(chat_histories=chat_histories, chatroom_id=use_id)
            else:
                prompt = memory.get_chat_history(chat_histories=chat_histories, chatroom_id=use_id)

            response_dict = MODEL.get_response(prompt)
            response = response_dict["content"]

            # Send reply and update histories
            LINEBOTHELPER.send_reply_message(event, response)
            memory.add_chat_history(chat_histories=chat_histories, chatroom_id=use_id, message=f"{configuration.BOT_CALL_NAME}: {response}")
            memory.add_model_responses(model_responses, use_id, response_dict)

        # Sync histories regardless of whether we responded
        memory.sync_to_pantry(basket_name=memory.PANTRY_CHAT_HISTORY, data=chat_histories)
        memory.sync_to_pantry(basket_name=memory.PANTRY_MODEL_RESPONSES, data=model_responses)
        if args.myfile is not None:
            memory.sync_to_pantry(basket_name=memory.PANTRY_MEDIA_METADATA, data=media_metadata)

    except Exception as e:
        print("Error processing event:", e)
        traceback.print_exc()
