from abc import ABC, abstractmethod
from core.container import Container
from core.database.models.user import UserModel


class Workflow(ABC):
  """
  Abstract base class for all Solomon workflows.
  """

  container: Container
  user: UserModel | None = None

  def __init__(self, container: Container) -> None:
    self.container = container

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
