from core.exceptions.UnauthorizedError import UnauthorizedError


class AuthenticationError(UnauthorizedError):
  """Raised when authentication credentials or verification codes are invalid."""

  pass
