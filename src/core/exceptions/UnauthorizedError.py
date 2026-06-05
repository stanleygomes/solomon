from core.exceptions.SolomonError import SolomonError


class UnauthorizedError(SolomonError):
  """Raised when authentication or authorization checks fail."""

  pass
