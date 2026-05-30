from loguru import logger
from core.dto.logger_config import LoggerConfig


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
