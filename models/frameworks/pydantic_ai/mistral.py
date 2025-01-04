import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel

from models import config

load_dotenv()

model = MistralModel(model_name=config.MISTRAL_MODEL, api_key=os.environ.get("MISTRAL_API_KEY"))
agent = Agent(model, system_prompt=config.SYSTEM_PROMPT)
