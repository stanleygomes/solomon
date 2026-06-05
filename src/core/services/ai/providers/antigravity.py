from core.services.ai.cli import CLIProvider


class AntigravityProvider(CLIProvider):
  """
  Antigravity implementation of the AIProvider interface.
  Uses the local agy CLI binary to generate text.
  """

  @property
  def binary_name(self) -> str:
    return "agy"

  @property
  def env_path_var(self) -> str:
    return "ANTIGRAVITY_PATH"

  def build_args(self, binary_path: str, prompt: str) -> list[str]:
    return [binary_path, "-p", prompt]
