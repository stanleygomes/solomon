from pydantic import BaseModel
from core.constants.message_role import MessageRole

class ChatMessageSchema(BaseModel):
  role: MessageRole
  content: str


class ChatCompletionsRequestSchema(BaseModel):
  model: str
  messages: list[ChatMessageSchema]


class ChoiceSchema(BaseModel):
  message: ChatMessageSchema


class ChatCompletionsResponseSchema(BaseModel):
  id: str
  object: str = "chat.completion"
  created: int
  model: str
  choices: list[ChoiceSchema]
