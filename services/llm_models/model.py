import os

from pydantic_ai import Agent  # Framework: Pydantic AI
import google.generativeai as genai  # Vanilla: Gemini
from mistralai import Mistral  # Vanilla: Mistral
from groq import Groq  # Vanilla: Groq
from dotenv import load_dotenv

import configuration

from utils import memory

load_dotenv()


class LLMModel:
    def __init__(self, system_prompt: str = configuration.SYSTEM_PROMPT, output_format=None):
        self.framework: str = configuration.FRAMEWORK
        self.provider: str = configuration.PROVIDER
        self.agent = None
        self.client = None
        self.system_prompt: str = system_prompt
        self.output_format = output_format
        self.responses: list[dict] = []

        # Initialize the model/agent based on the framework and provider
        if self.framework == "pydantic-ai":
            self._initialize_pydantic_ai()
        elif self.framework == "vanilla":
            self._initialize_vanilla_model()
        else:
            raise ValueError(f"Unsupported framework: {self.framework}. Choose between 'pydantic-ai' and 'vanila'")

    def _initialize_pydantic_ai(self):
        """
        Initialize the Pydantic AI agent.
        """
        if self.provider == "mistral":
            model_name = configuration.MISTRAL_MODEL
        elif self.provider == "gemini":
            model_name = configuration.GEMINI_MODEL
        elif self.provider == "groq":
            model_name = configuration.GROQ_MODEL
        else:
            raise ValueError(f"Unsupported provider for Pydantic AI: {self.provider}")

        self.agent = Agent(f"{self.provider}:{model_name}", system_prompt=self.system_prompt)

    def _initialize_vanilla_model(self):
        """
        Initialize the vanilla API client.
        """
        if self.provider == "mistral":
            self.agent = configuration.MISTRAL_MODEL
            self.client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))
        elif self.provider == "gemini":
            genai.configure(api_key=os.environ["GEMINI_API_KEY"])
            self.agent = genai.GenerativeModel(configuration.GEMINI_MODEL, system_instruction=self.system_prompt)
        elif self.provider == "groq":
            self.agent = configuration.GROQ_MODEL
            self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        else:
            raise ValueError(f"Unsupported provider for vanilla API: {self.provider}")

    def get_response(self, prompt: str, **kwargs) -> dict:
        """
        Generate a response using the initialized model/agent.

        Args:
            prompt (str): The input prompt for the LLM.
            **kwargs: Additional arguments for model-specific settings.

        Returns:
            dict: The generated response.
        """
        if self.framework == "pydantic-ai":
            return self._generate_response_pydantic_ai(prompt, **kwargs)
        elif self.framework == "vanilla":
            return self._generate_response_vanilla(prompt, **kwargs)
        else:
            raise ValueError(f"Unsupported framework: {self.framework}")

    def _generate_response_pydantic_ai(self, prompt: str, **kwargs):
        result = None
        response = self.agent.run_sync(prompt, **kwargs)
        self.responses.append(response)
        result = response.data
        return {"content": result}

    def _generate_response_vanilla(self, prompt: str, **kwargs):
        result = None
        if self.provider == "gemini":
            response = self.agent.generate_content(prompt, **kwargs)
            result = response.text
        elif self.provider == "groq" or self.provider == "mistral":
            response = self.client.chat.complete(
                model=self.agent, messages=[{"role": "system", "content": self.system_prompt}, {"role": "user", "content": prompt}], **kwargs
            )
            result = response.choices[0].message.content
        self.responses.append(response)
        return {"content": result}
