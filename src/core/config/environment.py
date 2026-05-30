import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
from core.dto.logger_config import LoggerConfig
from core.dto.mail_config import MailConfig
from core.dto.ai_config import AiConfig
from core.dto.db_config import DbConfig


load_dotenv()


@dataclass(frozen=True)
class Config:
  logger: LoggerConfig
  mail: MailConfig
  ai: AiConfig
  db: DbConfig

  @classmethod
  def load(cls) -> "Config":
    return cls(
      logger=LoggerConfig(
        path=Path(os.getenv("LOG_FILE")),
        level=os.getenv("LOG_LEVEL"),
        rotation=os.getenv("LOG_ROTATION"),
        retention=os.getenv("LOG_RETENTION"),
      ),
      mail=MailConfig(
        host=os.getenv("SMTP_HOST"),
        port=int(os.getenv("SMTP_PORT")),
        username=os.getenv("SMTP_USER"),
        password=os.getenv("SMTP_PASSWORD"),
        email_from=os.getenv("EMAIL_FROM", os.getenv("SMTP_USER", "")),
        email_to=os.getenv("EMAIL_TO", ""),
      ),
      ai=AiConfig(provider=os.getenv("AI_PROVIDER")),
      db=DbConfig(path=Path(os.getenv("DB_FILE"))),
    )
