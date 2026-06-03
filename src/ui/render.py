from textual.app import App
from ui.screens.chat_screen import ChatScreen
from core.constants.app import APP_VERSION, APP_NAME
from ui.constants.theme import RETRO_THEME


class Solomon(App[None]):
  """
  Solomon CLI
  """

  TITLE = f"{APP_NAME} v{APP_VERSION}"
  CSS_PATH = "../ui/styles/solomon.css"
  BINDINGS = [("ctrl+q", "quit", "Quit")]

  def __init__(self) -> None:
    """
    Initialize the application and register/set the retro theme.
    """
    super().__init__()
    self.register_theme(RETRO_THEME)
    self.theme = "retro"

  def on_mount(self) -> None:
    """
    Handle app mount event by pushing the chat screen.
    """
    self.push_screen(ChatScreen())
