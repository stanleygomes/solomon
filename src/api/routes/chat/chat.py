import time
import uuid
from fastapi import APIRouter, status
from core.constants.message_role import MessageRole
from api.routes.chat.schema import ChatCompletionsRequestSchema, ChatCompletionsResponseSchema, ChoiceSchema, ChatMessageSchema


router = APIRouter(tags=["Chat"])


@router.post(
  "/v1/chat/completions",
  response_model=ChatCompletionsResponseSchema,
  status_code=status.HTTP_200_OK,
  summary="OpenAI-compatible chat completions endpoint",
)
def chat_completions(
  payload: ChatCompletionsRequestSchema,
) -> ChatCompletionsResponseSchema:
  """
  Print messages and return mockup OpenAI-compatible chat completion.
  """
  print(payload.messages)

  completion_id = f"chatcmpl-{uuid.uuid4()}"
  created_time = int(time.time())

  assistant_message = ChatMessageSchema(
    role=MessageRole.ASSISTANT,
    content="Olá! Como posso ajudar você hoje?",
  )

  return ChatCompletionsResponseSchema(
    id=completion_id,
    created=created_time,
    model=payload.model,
    choices=[ChoiceSchema(message=assistant_message)],
  )
