import os
import subprocess
import shutil
from core.ai import AIProvider


class CopilotProvider(AIProvider):
  """
  GitHub Copilot implementation of the AIProvider interface.
  Uses the local copilot CLI binary to generate text.
  """

  def generate(self, prompt: str) -> str:
    copilot_path: str | None = os.getenv("COPILOT_PATH")
    if copilot_path:
      from pathlib import Path

      if not Path(copilot_path).exists():
        raise RuntimeError(
          f"Copilot binary not found at configured COPILOT_PATH: {copilot_path}"
        )
    else:
      copilot_path = shutil.which("copilot")

    if not copilot_path:
      raise RuntimeError(
        "GitHub Copilot CLI ('copilot') not found in PATH and COPILOT_PATH is not set"
      )

    process = subprocess.Popen(
      [copilot_path, "-s", "-p", prompt, "--no-ask-user", "--yolo"],
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      text=True,
    )

    stdout, stderr = process.communicate()

    if process.returncode != 0:
      raise RuntimeError(
        f"Copilot CLI error (Exit Code {process.returncode}): {stderr}"
      )

    output = stdout.strip()
    if not output:
      raise RuntimeError("Copilot CLI returned an empty response")

    return output
