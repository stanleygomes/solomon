import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from solomon.core.disk import DiskManager
from solomon.core.exceptions.DatabaseError import DatabaseError


class DatabaseManager:
  """
  Gerencia conexões e transações com o banco de dados SQLite.
  """

  def __init__(self, db_path: Path):
    self.db_path = db_path
    DiskManager.ensure_directory(self.db_path.parent)

  @contextmanager
  def connection(self) -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager para transações seguras no SQLite.
    Realiza commit automático em caso de sucesso ou rollback se ocorrer uma exceção.
    """
    conn = sqlite3.connect(self.db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row

    try:
      yield conn
      conn.commit()
    except Exception as e:
      conn.rollback()
      raise DatabaseError("Database connection or transaction failed") from e
    finally:
      conn.close()
