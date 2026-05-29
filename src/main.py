import sys
from loguru import logger
from core.config import Config
from core.render import Solomon
from core.logger import setup_logger


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

  logger.info("📋 Task: {}", task)
  logger.info("🚀 Application started")

  app = Solomon()
  app.run()


if __name__ == "__main__":
  main()
