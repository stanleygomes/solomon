from core.ai.cli import CLIProvider


class CopilotProvider(CLIProvider):
  """
  GitHub Copilot implementation of the AIProvider interface.
  Uses the local copilot CLI binary to generate text.
  """

  @property
  def binary_name(self) -> str:
    return "copilot"

  @property
  def env_path_var(self) -> str:
    return "COPILOT_PATH"

  def build_args(self, binary_path: str, prompt: str) -> list[str]:
    return [binary_path, "-s", "-p", prompt, "--no-ask-user", "--yolo"]
