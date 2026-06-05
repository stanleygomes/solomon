from abc import ABC, abstractmethod
from core.context import WorkflowContext


class Workflow(ABC):
  """
  Abstract base class for all Solomon workflows.
  """

  def __init__(self, context: WorkflowContext) -> None:
    self.context = context

  @abstractmethod
  def execute(self, input: str | None) -> str:
    """
    Executes the workflow logic.
    """
    pass

  @abstractmethod
  def should_execute(self) -> bool:
    """
    Determines whether the workflow should execute based on the context.
    By default, returns True. Override in subclasses for conditional execution.
    """
    return True
