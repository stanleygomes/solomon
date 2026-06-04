from enum import StrEnum


class MessageRole(StrEnum):
  """
  Enum representing the role of the message sender (agent or human).
  """

  AGENT = "agent"
  HUMAN = "human"
