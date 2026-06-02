from core.exceptions.SolomonError import SolomonError


class NotFoundError(SolomonError):
  """Raised when a requested resource or task is not found."""

  pass
