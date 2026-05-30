from markdown_it import MarkdownIt


class Markdown:
  """
  Utility class for parsing and converting Markdown text to HTML.
  """

  @staticmethod
  def to_html(text: str) -> str:
    """
    Converts GFM-flavor Markdown text to HTML.
    """
    md = MarkdownIt("gfm-like")
    return md.render(text)
