from typing import Any
from core.services.ai.factory import AIProviderFactory
from core.utils.disk import DiskUtils
from core.services.render.renderer import TemplateRenderer


class Prompt:
  """
  Service class for reading and executing prompt templates via the configured AI provider.
  """

  @staticmethod
  def execute(filename: str, context: dict[str, Any] | None = None) -> str:
    """
    Reads the prompt from the prompts folder, interpolates it with context if provided,
    and executes it using the configured AI provider.
    """
    prompts_dir = DiskUtils.resolve_path(__file__, "prompts")
    prompt_path = prompts_dir / filename

    prompt_content = DiskUtils.read_text(prompt_path)

    if context:
      prompt_content = TemplateRenderer.render_text(prompt_content, context)

    ai_provider = AIProviderFactory.generate()
    return ai_provider.generate(prompt_content)
