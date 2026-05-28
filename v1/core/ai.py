import os
import subprocess
import shutil
from abc import ABC, abstractmethod
from dotenv import load_dotenv


class AIProvider(ABC):
  @abstractmethod
  def generate(self, prompt: str) -> str:
    pass


class CopilotProvider(AIProvider):
  def generate(self, prompt: str) -> str:
    copilot_path: str | None = os.getenv("COPILOT_PATH")
    if copilot_path:
      from pathlib import Path
      if not Path(copilot_path).exists():
        raise RuntimeError(f"Copilot binary not found at configured COPILOT_PATH: {copilot_path}")
    else:
      copilot_path = shutil.which("copilot")

    if not copilot_path:
      raise RuntimeError("GitHub Copilot CLI ('copilot') not found in PATH and COPILOT_PATH is not set")

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


def get_ai_provider() -> AIProvider:
  load_dotenv()
  provider_type = os.getenv("AI_PROVIDER", "copilot").lower()

  if provider_type == "copilot":
    return CopilotProvider()
  else:
    raise ValueError(f"Unsupported AI provider: {provider_type}")
