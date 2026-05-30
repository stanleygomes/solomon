from core.ai.abstract import AIProvider
from core.config.environment import Config
from core.exceptions.UnsupportedAIProviderError import UnsupportedAIProviderError
from core.ai.providers.copilot import CopilotProvider
from core.ai.providers.antigravity import AntigravityProvider


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
      case "antigravity":
        return AntigravityProvider()
      case _:
        raise UnsupportedAIProviderError(f"Unsupported AI provider: {provider_type}")
