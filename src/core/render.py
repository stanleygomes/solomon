from textual.app import App
from textual.widgets import Button
from ui.screens.main_screen import MainScreen

class Solomon(App[None]):
  """
  Solomon Automation Hub main application.
  """

  CSS_PATH = "../ui/styles/solomon.css"
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

