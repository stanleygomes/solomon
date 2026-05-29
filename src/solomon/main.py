import sys
from loguru import logger
from solomon.core.config import Config
from solomon.core.render import Solomon


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

  logger.add(
    config.logger.path,
    rotation=config.logger.rotation,
    retention=config.logger.retention,
    level=config.logger.level,
    format="{time} {level} {message}",
  )

  task = get_task()

  logger.info("📋 Task: {}", task)
  logger.info("🚀 Application started")

  app = Solomon()
  app.run()


if __name__ == "__main__":
  main()
