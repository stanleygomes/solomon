import typer
from typing import Annotated
from cli.commands import ChatCommand, UpdateCommand

app = typer.Typer(
  name="solomon",
  help="👑 Solomon - Personal automation hub and task scheduler.",
  no_args_is_help=True,
  add_completion=False,
)


@app.command(name="chat", help="Send a message to Solomon and get a response.")
def chat(
  message: Annotated[str, typer.Argument(help="The message to send to Solomon")],
) -> None:
  """Send a message to Solomon."""
  ChatCommand().execute(message)


@app.command(name="update", help="Update Solomon to the latest version.")
def update_cli() -> None:
  """Update Solomon."""
  UpdateCommand().execute()


def main() -> None:
  """
  CLI application entry point.
  """
  app()


if __name__ == "__main__":
  main()
