from loguru import logger
from core.config.environment import Config
from cli.render import Solomon
from core.config.logger import setup_logger


def main() -> None:
  """
  CLI application entry point.
  """

  config = Config.load()

  setup_logger(config.logger)

  logger.info("🖥️ Launching TUI")
  app = Solomon()
  app.run()


if __name__ == "__main__":
  main()
