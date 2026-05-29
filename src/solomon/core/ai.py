from abc import ABC, abstractmethod
from solomon.core.config import Config
from solomon.core.exceptions.UnsupportedAIProviderError import UnsupportedAIProviderError
from solomon.core.providers.copilot import CopilotProvider


class AIProvider(ABC):
  @abstractmethod
  def generate(self, prompt: str) -> str:
    pass


def get_ai_provider() -> AIProvider:
  config = Config.load()
  provider_type = config.ai.provider

  match provider_type:
    case "copilot":
      return CopilotProvider()
    case _:
      raise UnsupportedAIProviderError(f"Unsupported AI provider: {provider_type}")
