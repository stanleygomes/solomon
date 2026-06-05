from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer


class BaseScreen(Screen[None]):
  """
  Base screen class that provides a standard layout with Header and Footer.
  Subclasses should override `compose_content` to render their specific widgets.
  """

  def compose(self) -> ComposeResult:
    """
    Base compose method yielding Header, screen-specific content, and Footer.
    """
    yield Header(show_clock=False)
    yield from self.compose_content()
    yield Footer()

  def compose_content(self) -> ComposeResult:
    """
    Override this method in subclasses to yield content between header and footer.
    """
    yield from ()
