import json
from typing import Any
from loguru import logger
from core.exceptions.ValidationError import ValidationError


class JsonUtils:
  """
  Utility class for cleaning, parsing, and handling JSON strings, especially from LLM responses.
  """

  @staticmethod
  def parse(text: str) -> Any:
    """
    Strips potential markdown code block backticks from LLM output and parses it into Python objects.
    """
    cleaned_output = text.strip()

    # Strip potential markdown block syntax if returned by the LLM (e.g. ```json ... ```)
    if cleaned_output.startswith("```"):
      lines = cleaned_output.splitlines()
      json_lines = [line for line in lines if not line.strip().startswith("```")]
      cleaned_output = "\n".join(json_lines)

    try:
      return json.loads(cleaned_output)
    except Exception as e:
      logger.error(
        "❌ Failed to parse JSON. Content length: {}. Error: {}", len(cleaned_output), e
      )
      raise ValidationError(f"Failed to parse cleaned JSON content: {e}") from e
