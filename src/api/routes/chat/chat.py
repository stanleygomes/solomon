from typing import cast
from fastapi import APIRouter, Depends, status, Request
from api.routes.chat.schema import (
  ChatCompletionsRequestSchema,
  ChatCompletionsResponseSchema,
  ChoiceSchema,
)
from api.dependencies.auth import verify_access_token
from core.container import Container
from core.database.repositories.user import UserRepository
from core.workflow.orchestrator import WorkflowOrchestrator
from core.exceptions.ValidationError import ValidationError
from core.exceptions.UnauthorizedError import UnauthorizedError


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
  _token_payload: dict[str, object] = Depends(verify_access_token),
) -> ChatCompletionsResponseSchema:
  """
  Print messages and return mockup OpenAI-compatible chat completion.
  """
  print(payload.messages)

  if not payload.messages:
    raise ValidationError("No messages provided")

  container = cast(Container, request.app.state.container)
  user_id = str(_token_payload.get("sub", ""))
  user_repo = UserRepository(container.db_manager)
  user = user_repo.find_by_id(user_id)
  if not user:
    raise UnauthorizedError("User not found")

  orchestrator = WorkflowOrchestrator(container)
  orchestrator_resp = orchestrator.execute(
    user=user,
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
