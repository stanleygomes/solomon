from core.config.environment import Config
from core.database.setup import DatabaseSetup
from core.database.migrator import DatabaseMigrator
from core.services.mail.mailer import Mailer
from core.database.repositories.task_execution import TaskExecutionRepository


class Container:
  """
  Dependency injection container for Solomon services.
  """

  config: Config
  db_manager: DatabaseSetup
  migrator: DatabaseMigrator
  mailer: Mailer
  task_execution_repo: TaskExecutionRepository

  def __init__(self, config: Config) -> None:
    self.config = config

    # 1. Database Setup & Migrations
    self.db_manager = DatabaseSetup(self.config.db.path)
    self.migrator = DatabaseMigrator(self.db_manager)

    # 2. Repositories
    self.task_execution_repo = TaskExecutionRepository(self.db_manager)

    # 3. Services
    self.mailer = Mailer(self.config.mail)

  def wire(self) -> None:
    """
    Run migrations and register dependencies.
    """
    self.migrator.migrate()
