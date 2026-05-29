import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
from solomon.core.dto.logger_config import LoggerConfig
from solomon.core.dto.mail_config import MailConfig
from solomon.core.dto.ai_config import AiConfig


load_dotenv()


@dataclass(frozen=True)
class Config:
  logger: LoggerConfig
  mail: MailConfig
  ai: AiConfig

  @classmethod
  def load(cls) -> "Config":
    return cls(
      logger=LoggerConfig(
        path=Path(os.getenv("LOG_FILE", "logs/app.log")),
        level=os.getenv("LOG_LEVEL", "INFO"),
        rotation=os.getenv("LOG_ROTATION", "10 MB"),
        retention=os.getenv("LOG_RETENTION", "10 days"),
      ),
      mail=MailConfig(
        host=os.getenv("SMTP_HOST", ""),
        port=int(os.getenv("SMTP_PORT", "587")),
        username=os.getenv("SMTP_USER", ""),
        password=os.getenv("SMTP_PASSWORD", ""),
      ),
      ai=AiConfig(provider=os.getenv("AI_PROVIDER", "copilot")),
    )
