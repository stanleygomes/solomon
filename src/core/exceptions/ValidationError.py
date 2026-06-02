from core.exceptions.SolomonError import SolomonError


class ValidationError(SolomonError):
  """Raised when input or output data format / JSON validation fails."""

  pass
