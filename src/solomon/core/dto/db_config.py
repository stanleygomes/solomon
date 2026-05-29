from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class DbConfig:
  """
  DTO for database configuration.
  """
  path: Path
