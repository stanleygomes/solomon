from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class AuthConfig:
  """
  Configuration for authentication settings.
  """

  cookie_secure: bool
  keys_dir: Path
  refresh_token_expiration: int
  magic_code_expiration: int
  jwt_algorithm: str
