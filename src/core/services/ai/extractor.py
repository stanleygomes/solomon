from core.services.ai.dto import ExtractedCommand


class CommandExtractor:
  """
  Extracts commands and arguments from chat messages.
  """

  @staticmethod
  def extract(content: str) -> ExtractedCommand:
    """
    Parses the message content to extract a command (e.g. /command) and text.
    """
    content = content.strip()
    if not content:
      return ExtractedCommand(command=None, text=None)

    if content.startswith("/"):
      parts = content.split(maxsplit=1)
      command = parts[0]
      text = parts[1] if len(parts) > 1 else None
      return ExtractedCommand(command=command, text=text)

    return ExtractedCommand(command=None, text=content)
