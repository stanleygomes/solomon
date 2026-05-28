from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Static


class MainScreen(Screen[None]):
    """
    Main screen displaying the base layout and controls.
    """

    def compose(self) -> ComposeResult:
        """
        Compose the child widgets of this screen.
        """
        yield Header()
        yield Footer()
        yield Static("Hello, world!", id="main_content")
        yield Button("Click me!", variant="primary", id="action_button")
