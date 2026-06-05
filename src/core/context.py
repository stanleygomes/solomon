from dataclasses import dataclass
from core.config.environment import Config
from core.database.setup import DatabaseSetup
from core.services.ai.abstract import AIProvider
from core.services.mail.mailer import Mailer
from core.database.repositories.task_execution import TaskExecutionRepository


@dataclass(frozen=True)
class WorkflowContext:
  """
  Execution context containing shared dependencies for Workflows.
  """

  config: Config
  db_manager: DatabaseSetup
  ai_provider: AIProvider
  mailer: Mailer
  task_execution_repo: TaskExecutionRepository
