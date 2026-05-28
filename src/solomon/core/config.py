import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
from solomon.core.dto.logger_config import LoggerConfig

load_dotenv()


@dataclass(frozen=True)
class Config:
  logger: LoggerConfig

  @classmethod
  def load(cls) -> "Config":
    return cls(
      logger=LoggerConfig(
        path=Path(os.getenv("LOG_FILE", "logs/app.log")),
        level=os.getenv("LOG_LEVEL", "INFO"),
        rotation=os.getenv("LOG_ROTATION", "10 MB"),
        retention=os.getenv("LOG_RETENTION", "10 days"),
      )
    )
