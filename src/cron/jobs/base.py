from abc import ABC, abstractmethod
from apscheduler.schedulers.blocking import BlockingScheduler
from core.container import Container


class CronJob(ABC):
  """
  Abstract base class for all Solomon cron jobs.
  """

  container: Container

  def __init__(self, container: Container) -> None:
    self.container = container

  @abstractmethod
  def register(self, scheduler: BlockingScheduler) -> None:
    """
    Registers the job with the APScheduler instance.
    """
    pass
