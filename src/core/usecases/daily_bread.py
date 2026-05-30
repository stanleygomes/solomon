from core.usecases.base import UseCase
from core.usecases.context import UseCaseContext
from loguru import logger


class DailyBreadUseCase(UseCase):
  """
  UseCase for generating and emailing the Daily Bread devotional.
  """

  def __init__(self, context: UseCaseContext) -> None:
    super().__init__(context)

  def should_execute(self) -> bool:
    """
    Checks if the Daily Bread devotional has already been successfully sent today.
    """
    from core.date import DateManager

    today = DateManager.today_str()
    if self.context.task_execution_repo.has_run_on_date("daily-bread", today):
      return False

    return True

  def execute(self) -> None:
    """
    Executes the Daily Bread email generation and delivery workflow.
    """
    logger.info("🚀 Executing Daily Bread UseCase workflow")
