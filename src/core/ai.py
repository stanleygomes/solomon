from abc import ABC, abstractmethod
from core.config import Config
from core.exceptions.UnsupportedAIProviderError import UnsupportedAIProviderError
from core.providers.copilot import CopilotProvider


class AIProvider(ABC):
  @abstractmethod
  def generate(self, prompt: str) -> str:
    pass

class AIProviderFactory:
  @staticmethod
  def generate() -> AIProvider:
    config = Config.load()
    provider_type = config.ai.provider

    match provider_type:
      case "copilot":
        return CopilotProvider()
      case _:
        raise UnsupportedAIProviderError(f"Unsupported AI provider: {provider_type}")
