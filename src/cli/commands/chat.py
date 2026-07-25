import typer
from loguru import logger
from core.config.environment import Config
from core.config.logger import setup_logger
from core.services.ai.factory import AIProviderFactory


class ChatCommand:
  """
  Command to send a message to Solomon and print the response.
  """

  def execute(self, message: str) -> None:
    """
    Send the message to the configured AI provider and stream the response to stdout.
    """
    config = Config.load()
    setup_logger(config.logger)
    logger.debug("💬 Sending message to AI provider: {}", message)

    try:
      ai_provider = AIProviderFactory.generate()
      response = ai_provider.generate(message)
      typer.echo(response)
    except Exception as e:
      logger.error("❌ Chat failed: {}", e)
      typer.echo(f"❌ Error: {e}", err=True)
      raise typer.Exit(code=1)
