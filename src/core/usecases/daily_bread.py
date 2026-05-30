from core.usecases.base import UseCase
from core.usecases.context import UseCaseContext
from loguru import logger


class DailyBreadUseCase(UseCase):
  """
  UseCase for generating and emailing the Daily Bread devotional.
  """

  def __init__(self, context: UseCaseContext) -> None:
    super().__init__(context)

  def execute(self) -> None:
    """
    Executes the Daily Bread email generation and delivery workflow.
    """
    logger.info("🚀 Executing Daily Bread UseCase workflow")
