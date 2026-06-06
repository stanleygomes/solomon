from enum import StrEnum


class MessageRole(StrEnum):
  """
  Enum representing the role of the message sender.
  """

  SYSTEM = "system"
  ASSISTANT = "assistant"
  USER = "user"
