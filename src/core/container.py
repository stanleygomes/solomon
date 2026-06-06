from core.config.environment import Config
from core.database.setup import DatabaseSetup
from core.database.migrator import DatabaseMigrator
from core.services.mail.mailer import Mailer
from core.services.auth.auth_service import AuthService
from core.database.repositories.task_execution import TaskExecutionRepository


class Container:
  """
  Dependency injection container for Solomon services.
  """

  config: Config
  db_manager: DatabaseSetup
  migrator: DatabaseMigrator
  mailer: Mailer
  auth_service: AuthService
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
    self.auth_service = AuthService(
      db_manager=self.db_manager,
      mailer=self.mailer,
      keys_dir=self.config.auth.keys_dir,
      refresh_token_expiration=self.config.auth.refresh_token_expiration,
      magic_code_expiration=self.config.auth.magic_code_expiration,
      jwt_algorithm=self.config.auth.jwt_algorithm,
    )

  def wire(self) -> None:
    """
    Run migrations and register dependencies.
    """
    self.migrator.migrate()
