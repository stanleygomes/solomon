import sys
from loguru import logger
from core.config import Config
from core.render import Solomon
from core.logger import setup_logger
from core.database import DatabaseManager
from core.usecases.orchestrator import UseCaseOrchestrator


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

  logger.info("🚀 Application started")

  db_manager = DatabaseManager(config.db.path)

  if task:
    orchestrator = UseCaseOrchestrator(config, db_manager)
    orchestrator.execute(task)
    return

  logger.info("🖥️ Launching TUI")
  app = Solomon()
  app.run()


if __name__ == "__main__":
  main()
