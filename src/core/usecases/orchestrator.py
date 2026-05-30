from loguru import logger
from core.config import Config
from core.database import DatabaseManager
from core.usecases.base import UseCase
from core.usecases.context import UseCaseContext
from core.constants.use_cases import USE_CASES
from core.exceptions.UnknownTaskError import UnknownTaskError


class UseCaseOrchestrator:
  """
  Orchestrator that instantiates and executes use cases based on task names.
  """

  def __init__(self, config: Config, db_manager: DatabaseManager) -> None:
    self.config = config
    self.db_manager = db_manager

  def execute(self, task_name: str) -> None:
    """
    Resolves, instantiates, and executes the specified use case.
    """
    logger.debug("🎯 Orchestrating execution of task: {}", task_name)

    use_case_cls = USE_CASES.get(task_name)
    if not use_case_cls:
      raise UnknownTaskError(f"Unknown task: {task_name}")

    # Resolve dependencies once inside a single context container DTO
    from core.ai_factory import AIProviderFactory
    from core.mailer import Mailer

    context = UseCaseContext(
      config=self.config,
      db_manager=self.db_manager,
      ai_provider=AIProviderFactory.generate(),
      mailer=Mailer(self.config.mail),
    )

    logger.debug("🎬 Instantiating Use Case: {}", use_case_cls.__name__)
    use_case: UseCase = use_case_cls(context)

    logger.debug("🚀 Executing Use Case: {}", use_case_cls.__name__)
    use_case.execute()

    logger.debug("✨ Use Case executed successfully: {}", use_case_cls.__name__)
