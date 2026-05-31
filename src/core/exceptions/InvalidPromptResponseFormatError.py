class InvalidPromptResponseFormatError(Exception):
  """Raised when the parsed JSON from the llm response does not conform to the expected format (e.g. not a list)."""

  pass
