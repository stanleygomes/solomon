from core.ai.factory import AIProviderFactory
from core.utils.disk import DiskManager


class Prompt:
  """
  Service class for reading and executing prompt templates via the configured AI provider.
  """

  @staticmethod
  def execute(filename: str) -> str:
    """
    Reads the prompt from the prompts folder and executes it using the configured AI provider.
    """
    prompts_dir = DiskManager.resolve_path(__file__, "prompts")
    prompt_path = prompts_dir / filename

    prompt_content = DiskManager.read_text(prompt_path)
    ai_provider = AIProviderFactory.generate()

    return ai_provider.generate(prompt_content)
