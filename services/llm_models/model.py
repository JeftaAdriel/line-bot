import os

from typing import Optional
from typing import Literal
from typing import Any
from pydantic import BaseModel

# from pydantic_ai import Agent  # Framework: Pydantic AI
import google.genai

# from mistralai import Mistral  # Vanilla: Mistral
# from groq import Groq  # Vanilla: Groq

import configuration


class ModelArgs(BaseModel):
    framework: Literal["pydantic-ai", "vanilla"] = configuration.FRAMEWORK
    provider: Literal["gemini", "groq", "mistral"] = configuration.PROVIDER
    system_prompt: str = configuration.SYSTEM_PROMPT
    output_format: Optional[Any] = None


class LLMModel:
    def __init__(self, model_args: ModelArgs):
        self.framework: str = model_args.framework
        self.provider: str = model_args.provider
        self.system_prompt: str = model_args.system_prompt
        self.output_format = model_args.output_format
        self.client = None
        self.model_name = None
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
            self.model_name = configuration.MISTRAL_MODEL
        elif self.provider == "gemini":
            self.model_name = configuration.GEMINI_MODEL
        elif self.provider == "groq":
            self.model_name = configuration.GROQ_MODEL
        else:
            raise ValueError(f"Unsupported provider for Pydantic AI: {self.provider}")

        # self.client = Agent(f"{self.provider}:{self.model_name}", system_prompt=self.system_prompt)

    def _initialize_vanilla_model(self):
        """
        Initialize the vanilla API client.
        """
        if self.provider == "gemini":
            self.model_name = configuration.GEMINI_MODEL
            self.client = google.genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        # elif self.provider == "mistral":
        #     self.model_name = configuration.MISTRAL_MODEL
        #     self.client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))
        # elif self.provider == "groq":
        #     self.model_name = configuration.GROQ_MODEL
        #     self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
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
        # result = None
        # response = self.client.run_sync(prompt, **kwargs)
        # self.responses.append(response)
        # result = response.data
        # return {"content": result}
        pass

    def _generate_response_vanilla(self, prompt: list):
        result = None
        response = None
        if self.provider == "gemini":
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=google.genai.types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    tools=[
                        google.genai.types.Tool(
                            google_search=google.genai.types.GoogleSearchRetrieval(
                                dynamic_retrieval_config=google.genai.types.DynamicRetrievalConfig(dynamic_threshold=0.6)
                            )
                        )
                    ],
                ),
            )
            result = response.text
        # elif self.provider in ["groq", "mistral"]:
        #     response = self.client.chat.complete(
        #         model=self.model_name, messages=[{"role": "system", "content": self.system_prompt}, {"role": "user", "content": prompt}], **kwargs
        #     )
        #     result = response.choices[0].message.content
        self.responses.append(response)
        return {"content": result}
