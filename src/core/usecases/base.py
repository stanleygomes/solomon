from abc import ABC, abstractmethod
from core.usecases.context import UseCaseContext


class UseCase(ABC):
  """
  Abstract base class for all Solomon use cases.
  """

  def __init__(self, context: UseCaseContext) -> None:
    self.context = context

  @abstractmethod
  def execute(self) -> None:
    """
    Executes the use case logic.
    """
    pass

  def should_execute(self) -> bool:
    """
    Determines whether the use case should execute based on the context.
    By default, returns True. Override in subclasses for conditional execution.
    """
    return True
