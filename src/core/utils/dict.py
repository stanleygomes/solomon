from dataclasses import asdict, is_dataclass
from typing import Any


class DictManager:
  """
  Utility class for handling dictionary conversions and operations.
  """

  @staticmethod
  def to_dict(context: object) -> dict[str, Any]:
    """
    Converts a dataclass or a dictionary context to a dictionary.
    """
    if is_dataclass(context) and not isinstance(context, type):
      return asdict(context)
    elif isinstance(context, dict):
      return context
    raise TypeError("Context must be a dataclass instance or a dictionary")
