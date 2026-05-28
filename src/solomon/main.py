from textual.app import App
from textual.widgets import Button
from solomon.ui.screens.main_screen import MainScreen
from loguru import logger
from solomon.core.config import Config


class Solomon(App[None]):
  """
  Solomon Automation Hub main application.
  """

  CSS_PATH = "styles/solomon.css"
  BINDINGS = [("q", "quit", "Quit")]

  def on_mount(self) -> None:
    """
    Handle app mount event by pushing the main screen.
    """
    self.push_screen(MainScreen())

  def on_button_pressed(self, event: Button.Pressed) -> None:
    """
    Handle button press events.
    """
    if event.button.id == "action_button":
      self.notify("Action button pressed!")


def main() -> None:
  config = Config.load()

  logger.add(
    config.logger.path,
    rotation=config.logger.rotation,
    retention=config.logger.retention,
    level=config.logger.level,
    format="{time} {level} {message}",
  )

  logger.info("🚀 Application started")
  app = Solomon()
  app.run()


if __name__ == "__main__":
  main()
