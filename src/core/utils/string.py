class StringManager:
  """
  Utility manager for string operations and sanitization.
  """

  @staticmethod
  def clean_email(email: str) -> str:
    """
    Sanitizes and normalizes an email address by trimming whitespace and lowercasing it.
    """
    return email.strip().lower()
