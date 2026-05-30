class UnknownTaskError(Exception):
  """Raised when the requested task name does not map to any registered UseCase."""

  pass
