from InquirerPy import inquirer
import typer
from loguru import logger
from core.config.environment import Config
from core.config.logger import setup_logger
from core.services.ai.factory import AIProviderFactory
from core.workflow.workflows import WORKFLOWS


class ChatCommand:
  """
  Command to select a workflow action, input prompt text, and execute.
  """

  def execute(self, action: str | None = None, message: str | None = None) -> None:
    """
    Prompt user for action and input if not provided, then send to AI provider.
    """
    config = Config.load()
    setup_logger(config.logger)

    available_actions = list(WORKFLOWS.keys())

    # Step 1: Select action if not provided via arguments
    selected_action = action
    if not selected_action:
      selected_action = inquirer.select(
        message="Select an action:",
        choices=available_actions,
      ).execute()

    if not selected_action:
      typer.echo("❌ Action is required.", err=True)
      raise typer.Exit(code=1)

    # Step 2: Input prompt text if not provided via arguments
    text_input = message
    if not text_input:
      text_input = inquirer.text(
        message=f"Enter message for {selected_action}:",
      ).execute()

    if text_input is None:
      raise typer.Exit(code=0)

    full_message = f"{selected_action} {text_input.strip()}".strip()

    logger.debug("💬 Sending full message to AI provider: {}", full_message)

    try:
      ai_provider = AIProviderFactory.generate()
      response = ai_provider.generate(full_message)
      typer.echo(response)
    except Exception as e:
      logger.error("❌ Chat failed: {}", e)
      typer.echo(f"❌ Error: {e}", err=True)
      raise typer.Exit(code=1)
