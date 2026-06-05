from loguru import logger
from textual import on, work
from textual.app import ComposeResult
from textual.widgets import Input, Static
from core.services.ai.factory import AIProviderFactory
from ui.screens.base_screen import BaseScreen
from ui.widgets.chat_history import ChatHistory
from ui.widgets.chat_input import ChatInput


class ChatScreen(BaseScreen):
  """
  Screen displaying the main chat interface.
  """

  def compose_content(self) -> ComposeResult:
    """
    Compose the specific content layout of this screen using custom widgets.
    """
    yield ChatHistory(id="chat_history")
    yield ChatInput(id="input_container")

  def on_mount(self) -> None:
    """
    Focus the input widget on mount.
    """
    self.query_one("#input_container", ChatInput).focus_input()

  @on(Input.Submitted, "#chat_input")
  def handle_chat_submitted(self, event: Input.Submitted) -> None:
    """
    Orchestrate flow when user submits a message.
    """
    message_text = event.value.strip()
    if not message_text:
      return

    # Clear input
    event.input.value = ""

    chat_history = self.query_one("#chat_history", ChatHistory)
    chat_history.add_user_message(message_text)
    placeholder = chat_history.add_thinking_placeholder()

    # Trigger background processor
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
        chat_history = self.query_one("#chat_history", ChatHistory)
        chat_history.scroll_to_widget(placeholder)

      self.app.call_from_thread(update_ui)
    except Exception as exc:
      logger.error("❌ Chat processing failed: {}", exc)
      error_msg = str(exc)

      def update_error() -> None:
        placeholder.update(f"❌ Error: {error_msg}")
        placeholder.remove_class("thinking")

      self.app.call_from_thread(update_error)
