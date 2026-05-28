from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class LoggerConfig:
  path: Path
  level: str
  rotation: str
  retention: str
