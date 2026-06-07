import typer
from typing import Annotated
from cli.commands import TuiCommand, StatusCommand

app = typer.Typer(
  name="solomon",
  help="👑 Solomon - Personal automation hub and task scheduler CLI client.",
  no_args_is_help=False,
  add_completion=False,
)


@app.callback(invoke_without_command=True)
def default_callback(ctx: typer.Context) -> None:
  """
  By default, launches the Terminal User Interface (TUI) if no command is specified.
  """
  if ctx.invoked_subcommand is None:
    TuiCommand().execute()


@app.command(name="tui", help="Launch the Terminal User Interface dashboard.")
def launch_tui() -> None:
  """Launch the Textual TUI dashboard."""
  TuiCommand().execute()


@app.command(
  name="status", help="Check the connection status of the remote Solomon API."
)
def check_status(
  url: Annotated[
    str, typer.Option(help="The status endpoint URL of the Solomon API")
  ] = "http://127.0.0.1:7000/status",
) -> None:
  """Check the Solomon API status."""
  StatusCommand().execute(url)


def main() -> None:
  """
  CLI application entry point.
  """
  app()


if __name__ == "__main__":
  main()
