from pathlib import Path


class DiskUtils:
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

  @staticmethod
  def resolve_path(base_file: str | Path, *parts: str) -> Path:
    """
    Resolves an absolute path relative to the directory of the specified base file.
    """
    return Path(base_file).parent.joinpath(*parts).resolve()


  @staticmethod
  def write_bytes(path: str | Path, data: bytes) -> None:
    """
    Writes binary data to a file.
    """
    Path(path).write_bytes(data)
