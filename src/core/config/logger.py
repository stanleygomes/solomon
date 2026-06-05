from loguru import logger
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class LoggerConfig:
  path: Path
  level: str
  rotation: str
  retention: str


def setup_logger(config: LoggerConfig) -> None:
  """
  Configure loguru logger globally using settings from LoggerConfig.
  """
  logger.add(
    config.path,
    rotation=config.rotation,
    retention=config.retention,
    level=config.level,
    format="{time} {level} {message}",
  )
