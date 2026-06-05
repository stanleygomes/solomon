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

  @staticmethod
  def now_plus_seconds(seconds: int) -> str:
    """
    Returns the current date and time in ISO format plus N seconds.
    """
    from datetime import timedelta

    return (datetime.now() + timedelta(seconds=seconds)).isoformat()

  @staticmethod
  def is_expired(iso_str: str) -> bool:
    """
    Checks if the given ISO format date and time is in the past.
    """
    return datetime.fromisoformat(iso_str) < datetime.now()
