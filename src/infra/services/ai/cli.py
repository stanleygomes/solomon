import os
import shutil
import subprocess
from abc import abstractmethod
from infra.services.ai.abstract import AIProvider
from core.utils.disk import DiskUtils
from core.exceptions.ExternalServiceError import ExternalServiceError


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
      if not DiskUtils.exists(custom_path):
        raise ExternalServiceError(
          f"{self.__class__.__name__} binary not found at configured {self.env_path_var}: {custom_path}"
        )
      binary_path = custom_path
    else:
      binary_path = shutil.which(self.binary_name)

    if not binary_path:
      raise ExternalServiceError(
        f"{self.__class__.__name__} CLI ('{self.binary_name}') not found in PATH and {self.env_path_var} is not set"
      )

    args = self.build_args(binary_path, prompt)

    process = subprocess.Popen(
      args,
      stdin=subprocess.DEVNULL,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      text=True,
    )

    try:
      stdout, stderr = process.communicate(timeout=30)
    except subprocess.TimeoutExpired as e:
      process.kill()
      # Read any remaining output after killing
      stdout, stderr = process.communicate()
      raise ExternalServiceError(
        f"{self.__class__.__name__} CLI execution timed out: {stderr}"
      ) from e

    if process.returncode != 0:
      raise ExternalServiceError(
        f"{self.__class__.__name__} CLI error (Exit Code {process.returncode}): {stderr}"
      )

    output = stdout.strip()
    if not output:
      raise ExternalServiceError(
        f"{self.__class__.__name__} CLI returned an empty response"
      )

    return output
