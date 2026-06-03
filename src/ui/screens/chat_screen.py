from loguru import logger
from textual.app import ComposeResult
from textual.widgets import Input, Static
from textual.containers import VerticalScroll, Horizontal
from textual import work
from core.ai.factory import AIProviderFactory
from ui.screens.base_screen import BaseScreen


class ChatScreen(BaseScreen):
  """
  Screen displaying the main chat interface.
  """

  def compose_content(self) -> ComposeResult:
    """
    Compose the specific content layout of this screen.
    """
    with VerticalScroll(id="chat_history"):
      yield Static(
        "🤖 Welcome to Solomon! Type a message below to chat.",
        classes="message ai-message",
      )
    with Horizontal(id="input_container"):
      yield Input(placeholder="Type your message here...", id="chat_input")

  def on_mount(self) -> None:
    """
    Set focus to the input widget when screen mounts.
    """
    self.query_one("#chat_input").focus()

  def on_input_submitted(self, event: Input.Submitted) -> None:
    """
    Handle the input submit event to send messages.
    """
    message_text = event.value.strip()
    if not message_text:
      return

    # Clear input
    event.input.value = ""

    # Mount user message
    chat_history = self.query_one("#chat_history")
    chat_history.mount(
      Static(f"👤 User: {message_text}", classes="message user-message")
    )

    # Mount thinking placeholder
    placeholder = Static(
      "⏳ Solomon is thinking...", classes="message ai-message thinking"
    )
    chat_history.mount(placeholder)

    # Scroll to the placeholder
    chat_history.scroll_to_widget(placeholder)

    # Trigger AI processing in background
    self.process_chat(message_text, placeholder)

  @work(thread=True)
  def process_chat(self, user_message: str, placeholder: Static) -> None:
    """
    Process chat message via the AI provider in a background thread to keep UI responsive.
    """
    logger.debug("💬 User sent message: {}", user_message)
    try:
      ai_provider = AIProviderFactory.generate()
      response = ai_provider.generate(user_message)

      def update_ui() -> None:
        placeholder.update(f"🤖 Solomon: {response}")
        placeholder.remove_class("thinking")
        chat_history = self.query_one("#chat_history")
        chat_history.scroll_to_widget(placeholder)

      self.app.call_from_thread(update_ui)
    except Exception as exc:
      logger.error("❌ Chat processing failed: {}", exc)
      error_msg = str(exc)

      def update_error() -> None:
        placeholder.update(f"❌ Error: {error_msg}")
        placeholder.remove_class("thinking")

      self.app.call_from_thread(update_error)
