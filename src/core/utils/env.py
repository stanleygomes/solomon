import os
from typing import Any
from core.exceptions.EnvironmentVariableNotFoundError import (
  EnvironmentVariableNotFoundError,
)

_UNDEFINED = object()


class EnvManager:
  """
  Utility class for managing environment variables.
  """

  @staticmethod
  def get(key: str, default: Any = _UNDEFINED) -> Any:
    """
    Gets the value of an environment variable. If not found and no default is provided,
    raises EnvironmentVariableNotFoundError.
    """
    val = os.environ.get(key)
    if val is not None:
      return val
    if default is not _UNDEFINED:
      return default
    raise EnvironmentVariableNotFoundError(
      f"Required environment variable '{key}' is missing."
    )
