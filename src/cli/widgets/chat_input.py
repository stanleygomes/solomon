from textual import events, on
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Input, OptionList
from textual.widgets.option_list import Option

AVAILABLE_SKILLS: list[str] = [
  "/daily-bread",
  "/scheduler",
  "/email-digest",
  "/compile-template",
]


class ChatInput(Vertical):
  """
  Widget encapsulating the text input and slash command suggestions popup.
  """

  def compose(self) -> ComposeResult:
    """
    Compose suggestions dropdown list and the text input field.
    """
    yield OptionList(id="command_suggestions")
    with Horizontal(id="input_field_container"):
      yield Input(placeholder="Type your message here...", id="chat_input")

  def focus_input(self) -> None:
    """
    Set focus to the text input field.
    """
    self.query_one("#chat_input", Input).focus()

  @on(Input.Changed, "#chat_input")
  def handle_input_changed(self, event: Input.Changed) -> None:
    """
    Show/hide autocomplete list when slash command is typed.
    """
    value = event.value.strip()
    suggestions = self.query_one("#command_suggestions", OptionList)

    if value.startswith("/") and " " not in value:
      matches = [s for s in AVAILABLE_SKILLS if s.startswith(value)]
      if matches:
        suggestions.clear_options()
        for match in matches:
          suggestions.add_option(Option(prompt=match, id=match))
        suggestions.styles.display = "block"
        return

    suggestions.styles.display = "none"

  @on(OptionList.OptionSelected, "#command_suggestions")
  def handle_option_selected(self, event: OptionList.OptionSelected) -> None:
    """
    Populate selected option into input field.
    """
    suggestions = self.query_one("#command_suggestions", OptionList)
    chat_input = self.query_one("#chat_input", Input)

    selected_option = str(event.option_id)
    chat_input.value = f"{selected_option} "
    chat_input.focus()
    chat_input.cursor_position = len(chat_input.value)
    suggestions.styles.display = "none"

  def on_key(self, event: events.Key) -> None:
    """
    Redirect arrow keys and alphanumeric typing between list and input field.
    """
    suggestions = self.query_one("#command_suggestions", OptionList)
    chat_input = self.query_one("#chat_input", Input)

    if chat_input.has_focus:
      if (
        event.key == "down"
        and suggestions.styles.display == "block"
        and suggestions.option_count > 0
      ):
        event.prevent_default()
        suggestions.focus()
        suggestions.highlighted = 0
    elif suggestions.has_focus:
      if event.key not in ("up", "down", "enter", "escape"):
        event.prevent_default()
        chat_input.focus()
        if event.is_printable and event.character:
          chat_input.value += event.character
          chat_input.cursor_position = len(chat_input.value)
        elif event.key == "backspace":
          chat_input.value = chat_input.value[:-1]
          chat_input.cursor_position = len(chat_input.value)
      elif event.key == "escape":
        event.prevent_default()
        chat_input.focus()
