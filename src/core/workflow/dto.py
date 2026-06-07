from dataclasses import dataclass
from core.services.ai.dto import ChatMessage


@dataclass(frozen=True)
class OrchestratorResponse:
  """
  DTO representing the response from the workflow orchestrator.
  """

  assistant_message: ChatMessage
  message_id: str
  created_time: int
