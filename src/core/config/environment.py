from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
from core.config.logger import LoggerConfig
from core.services.mail.config import MailConfig
from core.services.ai.config import AiConfig
from core.database.dto.db_config import DbConfig
from core.services.auth.config import AuthConfig
from core.utils.env import EnvManager


load_dotenv()


@dataclass(frozen=True)
class Config:
  logger: LoggerConfig
  mail: MailConfig
  ai: AiConfig
  db: DbConfig
  auth: AuthConfig

  @classmethod
  def load(cls) -> "Config":
    return cls(
      logger=LoggerConfig(
        path=Path(EnvManager.get("LOG_FILE")),
        level=EnvManager.get("LOG_LEVEL"),
        rotation=EnvManager.get("LOG_ROTATION"),
        retention=EnvManager.get("LOG_RETENTION"),
      ),
      mail=MailConfig(
        host=EnvManager.get("SMTP_HOST"),
        port=int(EnvManager.get("SMTP_PORT")),
        username=EnvManager.get("SMTP_USER"),
        password=EnvManager.get("SMTP_PASSWORD"),
        email_from=EnvManager.get("EMAIL_FROM"),
        email_to=EnvManager.get("EMAIL_TO"),
      ),
      ai=AiConfig(provider=EnvManager.get("AI_PROVIDER")),
      db=DbConfig(path=Path(EnvManager.get("DB_FILE"))),
      auth=AuthConfig(
        cookie_secure=EnvManager.get("COOKIE_SECURE") == "True",
        keys_dir=Path(EnvManager.get("KEYS_DIR")),
        refresh_token_expiration=int(EnvManager.get("REFRESH_TOKEN_EXPIRATION_SECONDS")),
        magic_code_expiration=int(EnvManager.get("MAGIC_CODE_EXPIRATION_SECONDS")),
        jwt_algorithm=EnvManager.get("JWT_ALGORITHM"),
      ),
    )
