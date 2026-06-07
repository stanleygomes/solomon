from loguru import logger
import typer
from core.config.environment import Config
from core.config.logger import setup_logger
from cli.render import Solomon
from cli.config import is_api_host_configured


class TuiCommand:
  """
  Command to launch the Solomon Terminal User Interface (TUI).
  """

  def execute(self) -> None:
    """
    Execute the TUI launch sequence after verifying host configuration.
    """
    if not is_api_host_configured():
      typer.echo("❌ Solomon API Host is not configured.")
      typer.echo("👉 Please configure it first by running:")
      typer.echo("   solomon config")
      raise typer.Exit(code=1)

    config = Config.load()
    setup_logger(config.logger)
    logger.info("🖥️ Launching TUI")
    tui_app = Solomon()
    tui_app.run()
