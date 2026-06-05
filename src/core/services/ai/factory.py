from core.services.ai.abstract import AIProvider
from core.config.environment import Config
from core.exceptions.PreconditionFailedError import PreconditionFailedError
from core.services.ai.providers.copilot import CopilotProvider
from core.services.ai.providers.antigravity import AntigravityProvider


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
        raise PreconditionFailedError(f"Unsupported AI provider: {provider_type}")
