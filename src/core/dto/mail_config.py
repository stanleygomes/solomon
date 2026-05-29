from dataclasses import dataclass


@dataclass(frozen=True)
class MailConfig:
  """
  Data Transfer Object for SMTP mail configuration.
  """
  host: str
  port: int
  username: str
  password: str
