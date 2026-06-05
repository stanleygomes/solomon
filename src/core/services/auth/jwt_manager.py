import jwt
from typing import Any


class JwtManager:
  """
  Manages encoding and decoding of JSON Web Tokens (JWT).
  """

  def __init__(self, algorithm: str) -> None:
    self.algorithm = algorithm

  def encode(self, payload: dict[str, Any], key: str) -> str:
    """
    Encodes a payload into a JWT using the private key and configured algorithm.
    """
    return jwt.encode(payload, key, algorithm=self.algorithm)

  def decode(self, token: str, key: str) -> dict[str, Any]:
    """
    Decodes and validates a JWT using the public/private key and configured algorithm.
    """
    return jwt.decode(token, key, algorithms=[self.algorithm])
