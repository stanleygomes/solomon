from pathlib import Path


class DiskManager:
  """
  Gerenciador de operações no disco (arquivos e pastas).
  """

  @staticmethod
  def ensure_directory(path: Path) -> None:
    """
    Garante que o diretório especificado exista, criando-o se necessário.
    """
    path.mkdir(parents=True, exist_ok=True)
