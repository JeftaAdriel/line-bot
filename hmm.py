import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from collections import deque

import configuration

load_dotenv()

agent = Agent(
    "gemini-1.5-flash",
    system_prompt="Be concise, reply with one sentence.",
)

result = agent.run_sync('Where does "hello world" come from?')
print(result.usage)
