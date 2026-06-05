from dataclasses import dataclass


@dataclass(frozen=True)
class TokenPair:
  """
  Represents a pair of access and refresh tokens.
  """

  access_token: str
  refresh_token: str
