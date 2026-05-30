from core.ai import AIProvider
from core.config import Config
from core.exceptions.UnsupportedAIProviderError import UnsupportedAIProviderError
from core.providers.copilot import CopilotProvider


class AIProviderFactory:
  """
  Factory to construct AIProvider instances based on configuration.
  """

  @staticmethod
  def generate() -> AIProvider:
    config = Config.load()
    provider_type = config.ai.provider

    match provider_type:
      case "copilot":
        return CopilotProvider()
      case _:
        raise UnsupportedAIProviderError(f"Unsupported AI provider: {provider_type}")
