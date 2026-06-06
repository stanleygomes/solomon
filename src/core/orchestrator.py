from loguru import logger
from core.config.environment import Config
from core.database.setup import DatabaseSetup
from core.workflow import Workflow
from core.context import WorkflowContext
from core.constants.use_cases import USE_CASES
from core.exceptions.NotFoundError import NotFoundError
from core.database.repositories.task_execution import TaskExecutionRepository
from core.utils.date import DateUtils
from core.constants.execution_status import ExecutionStatus


class WorkflowOrchestrator:
  """
  Orchestrator that instantiates and executes workflows based on task names.
  """

  def __init__(self, config: Config, db_manager: DatabaseSetup) -> None:
    self.config = config
    self.db_manager = db_manager

  def execute(self, task_name: str) -> None:
    """
    Resolves, instantiates, and executes the specified workflow.
    """
    logger.debug("🎯 Orchestrating execution of task: {}", task_name)

    workflow_cls = USE_CASES.get(task_name)
    if not workflow_cls:
      raise NotFoundError(f"Unknown task: {task_name}")

    # Initialize Repository
    repo = TaskExecutionRepository(self.db_manager)

    # Resolve dependencies once inside a single context container DTO
    from core.services.ai.factory import AIProviderFactory
    from core.services.mail.mailer import Mailer

    context = WorkflowContext(
      config=self.config,
      db_manager=self.db_manager,
      ai_provider=AIProviderFactory.generate(),
      mailer=Mailer(self.config.mail),
      task_execution_repo=repo,
    )

    logger.debug("🎬 Instantiating Workflow: {}", workflow_cls.__name__)
    workflow: Workflow = workflow_cls(context)

    # Validate execution conditional prerequisites
    if not workflow.should_execute():
      logger.warning(
        "🚫 Task '{}' execution pre-requisites not met. Skipping execution.", task_name
      )
      return

    logger.debug("🚀 Executing Workflow: {}", workflow_cls.__name__)
    try:
      workflow.execute()
      repo.save(
        task_name=task_name,
        status=ExecutionStatus.SUCCESS,
        executed_at=DateUtils.now_iso(),
      )
      logger.debug("✨ Workflow executed successfully: {}", workflow_cls.__name__)
    except Exception as e:
      repo.save(
        task_name=task_name,
        status=ExecutionStatus.FAILED,
        executed_at=DateUtils.now_iso(),
      )
      logger.error("❌ Use Case execution failed: {}", str(e))
      raise e
