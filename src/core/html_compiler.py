from dataclasses import asdict
from jinja2 import Template
from loguru import logger
from core.dto.theme import Theme
from core.disk import DiskManager


class HTMLCompiler:
  """
  Compiles base HTML and CSS templates using a specified Theme DTO.
  """

  @staticmethod
  def compile(theme: Theme) -> str:
    """
    Compiles base CSS with theme colors, injects it into base HTML, and returns the compiled template.
    """
    logger.debug("🛠️ Starting template compilation for theme: {}", theme.name)

    html_path = DiskManager.resolve_path(__file__, "templates", "base.html")
    css_path = DiskManager.resolve_path(__file__, "templates", "base.css")

    if not DiskManager.exists(html_path):
      raise FileNotFoundError(f"Base HTML template not found at {html_path}")

    if not DiskManager.exists(css_path):
      raise FileNotFoundError(f"Base CSS template not found at {css_path}")

    logger.debug("📖 Reading base templates from disk")
    css_template_content = DiskManager.read_text(css_path)
    html_template_content = DiskManager.read_text(html_path)

    # 1. Compile CSS with Theme
    logger.debug("🎨 Rendering CSS with theme colors")
    theme_dict = asdict(theme)
    css_template = Template(css_template_content)
    rendered_css = css_template.render(**theme_dict)

    # 2. Compile HTML with CSS Content
    logger.debug("📦 Injecting CSS into HTML template")
    html_template = Template(html_template_content)
    compiled_html = html_template.render(css_content=rendered_css)

    logger.info(
      "✨ Template compilation completed successfully for theme: {}", theme.name
    )
    return compiled_html
