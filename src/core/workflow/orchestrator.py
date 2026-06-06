from loguru import logger
from core.container import Container
from core.workflow.base import Workflow
from core.constants.use_cases import USE_CASES
from core.exceptions.NotFoundError import NotFoundError
from core.utils.date import DateUtils
from core.constants.execution_status import ExecutionStatus


class WorkflowOrchestrator:
  """
  Orchestrator that instantiates and executes workflows based on task names.
  """

  container: Container

  def __init__(self, container: Container) -> None:
    self.container = container

  def execute(self, task_name: str) -> None:
    """
    Resolves, instantiates, and executes the specified workflow.
    """
    logger.debug("🎯 Orchestrating execution of task: {}", task_name)

    workflow_cls = USE_CASES.get(task_name)
    if not workflow_cls:
      raise NotFoundError(f"Unknown task: {task_name}")

    repo = self.container.task_execution_repo

    logger.debug("🎬 Instantiating Workflow: {}", workflow_cls.__name__)
    workflow: Workflow = workflow_cls(self.container)

    # Validate execution conditional prerequisites
    if not workflow.should_execute():
      logger.warning(
        "🚫 Task '{}' execution pre-requisites not met. Skipping execution.", task_name
      )
      return

    logger.debug("🚀 Executing Workflow: {}", workflow_cls.__name__)
    try:
      workflow.execute("")
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
