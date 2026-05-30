from dataclasses import dataclass
from core.config import Config
from core.database import DatabaseManager
from core.ai import AIProvider
from core.mailer import Mailer
from core.repositories.task_execution import TaskExecutionRepository


@dataclass(frozen=True)
class UseCaseContext:
  """
  Execution context containing shared dependencies for UseCases.
  """

  config: Config
  db_manager: DatabaseManager
  ai_provider: AIProvider
  mailer: Mailer
  task_execution_repo: TaskExecutionRepository
