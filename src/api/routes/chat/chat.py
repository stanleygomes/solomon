from typing import cast
from fastapi import APIRouter, status, Request
from api.routes.chat.schema import (
  ChatCompletionsRequestSchema,
  ChatCompletionsResponseSchema,
  ChoiceSchema,
)
from core.container import Container
from core.workflow.orchestrator import WorkflowOrchestrator
from core.exceptions.ValidationError import ValidationError


router = APIRouter(tags=["Chat"])


@router.post(
  "/v1/chat/completions",
  response_model=ChatCompletionsResponseSchema,
  status_code=status.HTTP_200_OK,
  summary="OpenAI-compatible chat completions endpoint",
)
def chat_completions(
  payload: ChatCompletionsRequestSchema,
  request: Request,
) -> ChatCompletionsResponseSchema:
  """
  Receives a chat message and returns an OpenAI-compatible chat completion.
  """
  if not payload.messages:
    raise ValidationError("No messages provided")

  container = cast(Container, request.app.state.container)
  orchestrator = WorkflowOrchestrator(container)
  orchestrator_resp = orchestrator.execute(
    conversation_id=payload.id,
    message=payload.messages[-1],
  )

  assistant_message = orchestrator_resp.assistant_message

  return ChatCompletionsResponseSchema(
    id=orchestrator_resp.message_id,
    created=orchestrator_resp.created_time,
    model=payload.model,
    choices=[ChoiceSchema(message=assistant_message)],
  )
