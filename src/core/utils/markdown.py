from markdown_it import MarkdownIt


class MarkdownUtils:
  """
  Utility class for parsing and converting Markdown text to HTML.
  """

  @staticmethod
  def to_html(text: str) -> str:
    """
    Converts Markdown text to HTML using standard commonmark.
    """
    md = MarkdownIt("commonmark")
    return md.render(text)
