from loguru import logger
from core.config.environment import Config
from core.config.logger import setup_logger
from cli.render import Solomon


class TuiCommand:
  """
  Command to launch the Solomon Terminal User Interface (TUI).
  """

  def execute(self) -> None:
    """
    Execute the TUI launch sequence.
    """
    config = Config.load()
    setup_logger(config.logger)
    logger.info("🖥️ Launching TUI")
    tui_app = Solomon()
    tui_app.run()
