from datetime import datetime


class DateManager:
  """
  Utility manager for date and time helper operations.
  """

  @staticmethod
  def now_iso() -> str:
    """
    Returns the current date and time in ISO 8601 format.
    """
    return datetime.now().isoformat()

  @staticmethod
  def today_str() -> str:
    """
    Returns the current date in YYYY-MM-DD format.
    """
    return datetime.now().strftime("%Y-%m-%d")
