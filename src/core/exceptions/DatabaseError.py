from core.exceptions.SolomonError import SolomonError


class DatabaseError(SolomonError):
  """Raised when a database connection or query execution fails."""

  pass
