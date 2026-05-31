class EnvironmentVariableNotFoundError(Exception):
  """Raised when a required environment variable is not set and no default value is provided."""

  pass
