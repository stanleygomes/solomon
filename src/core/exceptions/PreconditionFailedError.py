from core.exceptions.SolomonError import SolomonError


class PreconditionFailedError(SolomonError):
  """Raised when execution prerequisites or configurations are not met."""

  pass
