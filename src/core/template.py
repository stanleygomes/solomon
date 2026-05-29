from dataclasses import asdict, is_dataclass
from jinja2 import Template
from loguru import logger
from core.html_compiler import HTMLCompiler
from core.dto.theme import Theme


class TemplateRenderer:
  """
  Renderer for HTML templates using HTMLCompiler and Jinja2.
  """

  @staticmethod
  def render(theme: Theme, context: object) -> str:
    """
    Compiles the HTML template using the theme and renders it with the provided DTO (dataclass) context.
    """
    logger.debug("🎬 Rendering template for theme: {}", theme.name)

    compiled_template = HTMLCompiler.compile(theme)

    if is_dataclass(context) and not isinstance(context, type):
      ctx_dict = asdict(context)
    elif isinstance(context, dict):
      ctx_dict = context
    else:
      raise TypeError("Context must be a dataclass instance or a dictionary")

    template = Template(compiled_template)
    rendered_content = template.render(**ctx_dict)

    logger.debug("✨ Template rendered successfully")
    return rendered_content
