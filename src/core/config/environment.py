from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
from core.config.logger import LoggerConfig
from core.services.mail.config import MailConfig
from core.services.ai.config import AiConfig
from core.database.dto.db_config import DbConfig
from core.utils.env import EnvUtils


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
        path=Path(EnvUtils.get("LOG_FILE")),
        level=EnvUtils.get("LOG_LEVEL"),
        rotation=EnvUtils.get("LOG_ROTATION"),
        retention=EnvUtils.get("LOG_RETENTION"),
      ),
      mail=MailConfig(
        host=EnvUtils.get("SMTP_HOST"),
        port=int(EnvUtils.get("SMTP_PORT")),
        username=EnvUtils.get("SMTP_USER"),
        password=EnvUtils.get("SMTP_PASSWORD"),
        email_from=EnvUtils.get("EMAIL_FROM"),
        email_to=EnvUtils.get("EMAIL_TO"),
      ),
      ai=AiConfig(provider=EnvUtils.get("AI_PROVIDER")),
      db=DbConfig(path=Path(EnvUtils.get("DB_FILE"))),
    )
