from abc import ABC, abstractmethod
from core.database.setup import DatabaseSetup


class BaseSeeder(ABC):
  """
  Abstract base class for all database seeders.
  """

  @abstractmethod
  def seed(self, db_manager: DatabaseSetup) -> None:
    """
    Executes the seeding logic for a specific model or set of models.
    """
    pass
