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

  @staticmethod
  def exists(path: str | Path) -> bool:
    """
    Checks if the specified path exists on disk.
    """
    return Path(path).exists()

  @staticmethod
  def read_text(path: str | Path) -> str:
    """
    Reads and returns the text content of a file.
    """
    return Path(path).read_text(encoding="utf-8")
