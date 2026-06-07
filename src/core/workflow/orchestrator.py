from loguru import logger
from core.container import Container
from core.workflow.base import Workflow
from core.workflow.workflows import WORKFLOWS
from core.exceptions.NotFoundError import NotFoundError
from core.utils.date import DateUtils
from core.constants.execution_status import ExecutionStatus
from core.database.models.user import UserModel
from core.services.ai.dto import ChatMessage
from core.database.repositories.conversation import ConversationRepository
from core.database.repositories.message import MessageRepository
from core.constants.message_role import MessageRole


class WorkflowOrchestrator:
  """
  Orchestrator that instantiates and executes workflows based on task names.
  """

  container: Container

  def __init__(self, container: Container) -> None:
    self.container = container

  def execute(
    self,
    workflow_name: str,
    user: UserModel | None = None,
    conversation_id: str | None = None,
    message: ChatMessage | None = None,
  ) -> str | None:
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
    workflow.user = user
    workflow.conversation_id = conversation_id
    workflow.message = message

    # Validate execution conditional prerequisites
    if not workflow.should_execute():
      logger.warning(
        "🚫 Task '{}' execution pre-requisites not met. Skipping execution.",
        workflow_name,
      )
      return None

    # Persist user message and create conversation if not exists
    if message:
      if not conversation_id and user:
        title = message.content[:50]
        conv_repo = ConversationRepository(self.container.db_manager)
        conv = conv_repo.create(user_id=str(user.id), title=title)
        conversation_id = str(conv.id)
        workflow.conversation_id = conversation_id

      if conversation_id:
        msg_repo = MessageRepository(self.container.db_manager)
        _ = msg_repo.create(
          conversation_id=conversation_id,
          role=MessageRole.USER,
          content=message.content,
        )

    logger.debug("🚀 Executing Workflow: {}", workflow_name)
    try:
      workflow_response: str | None = workflow.execute("")
      repo.save(
        task_name=workflow_name,
        status=ExecutionStatus.SUCCESS,
        executed_at=DateUtils.now_iso(),
      )
      logger.debug("✨ Workflow executed successfully: {}", workflow_name)

      # Persist assistant response
      if conversation_id and workflow_response:
        msg_repo = MessageRepository(self.container.db_manager)
        _ = msg_repo.create(
          conversation_id=conversation_id,
          role=MessageRole.ASSISTANT,
          content=workflow_response,
        )

      return workflow_response
    except Exception as e:
      repo.save(
        task_name=workflow_name,
        status=ExecutionStatus.FAILED,
        executed_at=DateUtils.now_iso(),
      )
      logger.error("❌ Use Case execution failed: {}", str(e))
      raise e
