import typer
from typing import Annotated
from cli.commands import ChatCommand, UpdateCommand

app = typer.Typer(
  name="solomon",
  help="👑 Solomon - Personal automation hub and task scheduler.",
  no_args_is_help=True,
  add_completion=False,
)


@app.command(name="chat", help="Send a message to Solomon in 2 steps or via arguments.")
def chat(
  action: Annotated[
    str | None,
    typer.Argument(help="Optional action (e.g. /daily-bread)"),
  ] = None,
  message: Annotated[
    str | None,
    typer.Argument(help="Optional message content"),
  ] = None,
) -> None:
  """Send a message to Solomon."""
  ChatCommand().execute(action=action, message=message)


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
