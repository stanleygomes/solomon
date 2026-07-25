from abc import ABC, abstractmethod
from core.container import Container
from core.services.ai.dto import ChatMessage


class Workflow(ABC):
  """
  Abstract base class for all Solomon workflows.
  """

  container: Container
  conversation_id: str | None = None
  message: ChatMessage | None = None

  def __init__(self, container: Container) -> None:
    self.container = container

  @abstractmethod
  def execute(self, input: str | None = None) -> str | None:
    """
    Executes the workflow logic.
    """
    pass

  def should_execute(self) -> bool:
    """
    Determines whether the workflow should execute based on the context.
    By default, returns True. Override in subclasses for conditional execution.
    """
    return True
