import sys
from loguru import logger
from core.config.environment import Config
from ui.render import Solomon
from core.config.logger import setup_logger
from core.database.setup import DatabaseSetup
from core.database.migrator import DatabaseMigrator
from core.utils.disk import DiskManager
from core.orchestrator import UseCaseOrchestrator


def get_task() -> str | None:
  """
  Retrieve task argument from command line.
  """
  return sys.argv[1] if len(sys.argv) > 1 else None


def main() -> None:
  """
  Main application entry point.
  """

  config = Config.load()

  setup_logger(config.logger)

  task = get_task()

  db_manager = DatabaseSetup(config.db.path)

  migrations_dir = DiskManager.resolve_path(__file__, "core", "migrations")
  migrator = DatabaseMigrator(db_manager, migrations_dir)
  migrator.migrate()

  if task:
    logger.info("🚀 Executing...")
    orchestrator = UseCaseOrchestrator(config, db_manager)
    orchestrator.execute(task)
    return

  logger.info("🖥️ Launching TUI")
  app = Solomon()
  app.run()


if __name__ == "__main__":
  main()
