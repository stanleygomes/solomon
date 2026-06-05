from jinja2 import Template
from loguru import logger
from core.services.render.compiler import HTMLCompiler
from core.services.render.theme import Theme
from core.utils.dict import DictManager


class TemplateRenderer:
  """
  Renderer for HTML templates and text template strings using HTMLCompiler and Jinja2.
  """

  @staticmethod
  def render_html(theme: Theme, context: object) -> str:
    """
    Compiles the HTML template using the theme and renders it with the provided DTO (dataclass) context.
    """
    logger.debug("🎬 Rendering template for theme: {}", theme.name)

    compiled_template = HTMLCompiler.compile(theme)
    ctx_dict = DictManager.to_dict(context)

    template = Template(compiled_template)
    rendered_content = template.render(**ctx_dict)

    logger.debug("✨ Template rendered successfully")
    return rendered_content

  @staticmethod
  def render_text(template_content: str, context: object) -> str:
    """
    Renders a raw template text using the provided context.
    """
    logger.debug("🎬 Rendering text template")
    ctx_dict = DictManager.to_dict(context)

    template = Template(template_content)
    rendered_content = template.render(**ctx_dict)

    logger.debug("✨ Text template rendered successfully")
    return rendered_content
