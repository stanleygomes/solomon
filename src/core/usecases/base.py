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
