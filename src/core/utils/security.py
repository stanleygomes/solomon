import secrets


class SecurityUtils:
  """
  Utility manager for security and cryptographic operations.
  """

  @staticmethod
  def generate_numeric_code(length: int = 6) -> str:
    """
    Generates a cryptographically secure random numeric code of the specified length.
    """
    return "".join(secrets.choice("0123456789") for _ in range(length))
