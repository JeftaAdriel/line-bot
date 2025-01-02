import config
import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel

load_dotenv()

model = MistralModel(model_name="pixtral-12b-2409", api_key=os.environ.get("MISTRAL_API_KEY"))
agent = Agent(model, system_prompt=config.SYSTEM_PROMPT)
