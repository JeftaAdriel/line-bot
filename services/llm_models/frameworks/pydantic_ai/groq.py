import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

import config

load_dotenv()

model = GroqModel(model_name=config.GROQ_MODEL, api_key=os.environ.get("GROQ_API_KEY"))
agent = Agent(model, system_prompt=config.SYSTEM_PROMPT)
