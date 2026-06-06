from pydantic import BaseModel
from core.services.ai.dto import ChatMessage


class ChatCompletionsRequestSchema(BaseModel):
  id: str | None
  model: str
  messages: list[ChatMessage]


class ChoiceSchema(BaseModel):
  message: ChatMessage


class ChatCompletionsResponseSchema(BaseModel):
  id: str
  object: str = "chat.completion"
  created: int
  model: str
  choices: list[ChoiceSchema]
