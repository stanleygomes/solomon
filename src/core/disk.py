from pathlib import Path


class DiskManager:
  """
  Manager for disk operations (files and directories).
  """

  @staticmethod
  def ensure_directory(path: Path) -> None:
    """
    Ensures that the specified directory exists, creating it if necessary.
    """
    path.mkdir(parents=True, exist_ok=True)
