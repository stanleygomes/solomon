from pathlib import Path
from dataclasses import asdict, is_dataclass
from jinja2 import Template
from loguru import logger
from core.disk import DiskManager


class TemplateRenderer:
  """
  Renderer for HTML/text templates using Jinja2.
  """

  @staticmethod
  def render(template_path: str | Path, context: object) -> str:
    """
    Renders a template from disk using the provided DTO (dataclass) context.
    """
    logger.info("Rendering template from path: {}", template_path)

    if not DiskManager.exists(template_path):
      logger.error("Template file not found: {}", template_path)
      raise FileNotFoundError(f"Template file not found: {template_path}")

    template_content = DiskManager.read_text(template_path)

    if is_dataclass(context) and not isinstance(context, type):
      ctx_dict = asdict(context)
    elif isinstance(context, dict):
      ctx_dict = context
    else:
      logger.error("Invalid context type provided: {}", type(context))
      raise TypeError("Context must be a dataclass instance or a dictionary")

    template = Template(template_content)
    rendered_content = template.render(**ctx_dict)

    logger.info("Template rendered successfully")
    return rendered_content
