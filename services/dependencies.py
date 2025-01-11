from pydantic import BaseModel
from utils.line_related import LineBotHelper


class ChatbotInput(BaseModel):
    LineBotHelper: LineBotHelper
