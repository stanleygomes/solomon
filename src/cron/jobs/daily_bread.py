from typing import override
from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler
from core.services.ai.dto import ChatMessage
from core.constants.message_role import MessageRole
from core.database.repositories.user import UserRepository
from core.workflow.orchestrator import WorkflowOrchestrator
from cron.jobs.base import CronJob


class DailyBreadJob(CronJob):
  """
  Cron job for executing the Daily Bread workflow.
  """

  @override
  def register(self, scheduler: BlockingScheduler) -> None:
    """
    Registers the job with the APScheduler instance.
    """
    _ = scheduler.add_job(
      self.execute,
      trigger="cron",
      hour=8,
      minute=0,
      id="daily-bread-job",
    )

  def execute(self) -> None:
    """
    Executes the Daily Bread workflow in-process.
    """
    logger.info("⏰ Triggering scheduled Daily Bread job")

    user_repo = UserRepository(self.container.db_manager)
    users = user_repo.get_all()
    if not users:
      logger.error("❌ No users found in database. Skipping Daily Bread execution.")
      return

    message = ChatMessage(role=MessageRole.USER, content="/daily-bread")
    orchestrator = WorkflowOrchestrator(self.container)

    for user in users:
      logger.info("👉 Processing Daily Bread for user: {}", user.email)
      try:
        _ = orchestrator.execute(user=user, message=message)
        logger.info(
          "✨ Scheduled Daily Bread job completed successfully for {}", user.email
        )
      except Exception as e:
        logger.error("❌ Scheduled Daily Bread job failed for {}: {}", user.email, e)
