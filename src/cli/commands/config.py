from InquirerPy import inquirer
import typer
from cli.config import get_api_host, save_api_host


class ConfigCommand:
  """
  Command to configure local Solomon CLI settings.
  """

  def execute(self) -> None:
    """
    Prompt the user for Solomon API host URL and save it to config.toml.
    """
    current_host = get_api_host()

    host = inquirer.text(
      message="Enter the Solomon API Host URL (IP or domain):",
      default=current_host,
    ).execute()

    if host is not None:
      host = host.strip()
      if host:
        save_api_host(host)
        typer.echo(f"✅ API Host successfully updated to: {host}")
      else:
        typer.echo("⚠️ Host URL cannot be empty.")
