from dataclasses import dataclass
from core.constants.message_role import MessageRole


@dataclass(frozen=True)
class ChatMessage:
  """
  Domain representation of a chat message.
  """

  role: MessageRole
  content: str


@dataclass(frozen=True)
class ExtractedCommand:
  """
  DTO representing an extracted command and its parameters.
  """

  command: str | None
  text: str | None
