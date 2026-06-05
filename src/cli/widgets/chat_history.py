from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static


class ChatHistory(VerticalScroll):
  """
  Widget representing the scrollable chat history log.
  """

  def compose(self) -> ComposeResult:
    """
    Compose the initial welcome message from Solomon.
    """
    yield Static(
      "🤖 Welcome to Solomon! Type a message below to chat.",
      classes="message ai-message",
    )

  def add_user_message(self, message: str) -> None:
    """
    Append a user message to the history and scroll it into view.
    """
    msg_widget = Static(f"👤 User: {message}", classes="message user-message")
    self.mount(msg_widget)
    self.scroll_to_widget(msg_widget)

  def add_thinking_placeholder(self) -> Static:
    """
    Append a thinking placeholder and scroll it into view.
    """
    placeholder = Static(
      "⏳ Solomon is thinking...", classes="message ai-message thinking"
    )
    self.mount(placeholder)
    self.scroll_to_widget(placeholder)
    return placeholder
