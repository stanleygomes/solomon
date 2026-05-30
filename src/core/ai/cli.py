import os
import shutil
import subprocess
from abc import abstractmethod
from core.ai.abstract import AIProvider
from core.utils.disk import DiskManager
from core.exceptions.AIProviderError import AIProviderError


class CLIProvider(AIProvider):
  """
  Abstract base class for command-line interface based AI providers.
  """

  @property
  @abstractmethod
  def binary_name(self) -> str:
    """
    The default name of the CLI binary.
    """
    pass

  @property
  @abstractmethod
  def env_path_var(self) -> str:
    """
    The name of the environment variable specifying the custom binary path.
    """
    pass

  @abstractmethod
  def build_args(self, binary_path: str, prompt: str) -> list[str]:
    """
    Builds the command line arguments list.
    """
    pass

  def generate(self, prompt: str) -> str:
    """
    Generates a response by executing the CLI binary with the given prompt.
    """
    custom_path = os.getenv(self.env_path_var)
    if custom_path:
      if not DiskManager.exists(custom_path):
        raise AIProviderError(
          f"{self.__class__.__name__} binary not found at configured {self.env_path_var}: {custom_path}"
        )
      binary_path = custom_path
    else:
      binary_path = shutil.which(self.binary_name)

    if not binary_path:
      raise AIProviderError(
        f"{self.__class__.__name__} CLI ('{self.binary_name}') not found in PATH and {self.env_path_var} is not set"
      )

    args = self.build_args(binary_path, prompt)

    process = subprocess.Popen(
      args,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      text=True,
    )

    stdout, stderr = process.communicate()

    if process.returncode != 0:
      raise AIProviderError(
        f"{self.__class__.__name__} CLI error (Exit Code {process.returncode}): {stderr}"
      )

    output = stdout.strip()
    if not output:
      raise AIProviderError(f"{self.__class__.__name__} CLI returned an empty response")

    return output
