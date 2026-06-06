import time
import uuid
from fastapi import APIRouter, Depends, status
from core.constants.message_role import MessageRole
from api.routes.chat.schema import (
  ChatCompletionsRequestSchema,
  ChatCompletionsResponseSchema,
  ChoiceSchema,
)
from core.services.ai.dto import ChatMessage
from api.dependencies.auth import verify_access_token


router = APIRouter(tags=["Chat"])


@router.post(
  "/v1/chat/completions",
  response_model=ChatCompletionsResponseSchema,
  status_code=status.HTTP_200_OK,
  summary="OpenAI-compatible chat completions endpoint",
)
def chat_completions(
  payload: ChatCompletionsRequestSchema,
  _token_payload: dict[str, object] = Depends(verify_access_token),
) -> ChatCompletionsResponseSchema:
  """
  Print messages and return mockup OpenAI-compatible chat completion.
  """
  print(payload.messages)

  completion_id = f"chatcmpl-{uuid.uuid4()}"
  created_time = int(time.time())

  assistant_message = ChatMessage(
    role=MessageRole.ASSISTANT,
    content="Olá! Como posso ajudar você hoje?",
  )

  return ChatCompletionsResponseSchema(
    id=completion_id,
    created=created_time,
    model=payload.model,
    choices=[ChoiceSchema(message=assistant_message)],
  )
