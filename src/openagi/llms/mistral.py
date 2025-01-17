from openagi.exception import OpenAGIException
from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.utils.yamlParse import read_from_env

import logging
from typing import Any
from langchain_core.messages import HumanMessage

try:
   from langchain_mistralai import ChatMistralAI
except ImportError:
  raise OpenAGIException("Install langchain Mistral AI with cmd `pip install langchain_mistralai`")


class MistralConfigModel(LLMConfigModel):
    """Configuration model for Mistral."""

    mistral_api_key: str
    model_name: str = "mistral-large-latest"
    temperature: float = 0.1

class MistralModel(LLMBaseModel):
    """Mistral service implementation of the LLMBaseModel.

    This class implements the specific logic required to work with Mistral service.
    """

    config: Any

    def load(self):
        """Initializes the Mistral instance with configurations."""
        self.llm = ChatMistralAI(
           model = self.config.model_name,
           temperature = self.config.temperature,
           api_key = self.config.mistral_api_key
        )
        return self.llm

    async def async_load(self):
        return self.load()

    def run(self, input_text: str):
        """Runs the Mistral model with the provided input text.

        Args:
            input_text: The input text to process.

        Returns:
            The response from Mistral service.
        """
        logging.info(f"Running LLM - {self.__class__.__name__}")
        self.load_llm()
        message = self.process_message(input_data=input_text)
        resp = self.llm([message])
        return resp.content

    async def async_run(self, input_text: str):
        """Runs the Mistral model with the provided input text.

        Args:
            input_text: The input text to process.

        Returns:
            The response from Mistral service.
        """
        logging.info(f"Running LLM - {self.__class__.__name__}")
        self.load_llm()
        message = self.process_message(input_data=input_text)
        resp = await self.llm.ainvoke([message])
        return resp.content

    @staticmethod
    def load_from_env_config() -> MistralConfigModel:
        """Loads the Mistral configurations from a YAML file.

        Returns:
            An instance of MistralConfigModel with loaded configurations.
        """
        return MistralConfigModel(
            mistral_api_key=read_from_env("MISTRAL_API_KEY", raise_exception=True),
        )