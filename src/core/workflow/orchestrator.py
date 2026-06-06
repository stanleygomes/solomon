from loguru import logger
from core.container import Container
from core.workflow.base import Workflow
from core.workflow.workflows import WORKFLOWS
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

  def execute(self, workflow_name: str) -> None:
    """
    Resolves, instantiates, and executes the specified workflow.
    """
    logger.debug("🎯 Orchestrating execution of workflow: {}", workflow_name)

    workflow = WORKFLOWS.get(workflow_name)
    if not workflow:
      raise NotFoundError(f"Unknown workflow: {workflow_name}")

    repo = self.container.task_execution_repo

    logger.debug("🎬 Instantiating Workflow: {}", workflow_name)
    workflow: Workflow = workflow(self.container)

    # Validate execution conditional prerequisites
    if not workflow.should_execute():
      logger.warning(
        "🚫 Task '{}' execution pre-requisites not met. Skipping execution.", workflow_name
      )
      return

    logger.debug("🚀 Executing Workflow: {}", workflow_name)
    try:
      workflow.execute("")
      repo.save(
        task_name=workflow_name,
        status=ExecutionStatus.SUCCESS,
        executed_at=DateUtils.now_iso(),
      )
      logger.debug("✨ Workflow executed successfully: {}", workflow_name)
    except Exception as e:
      repo.save(
        task_name=workflow_name,
        status=ExecutionStatus.FAILED,
        executed_at=DateUtils.now_iso(),
      )
      logger.error("❌ Use Case execution failed: {}", str(e))
      raise e
