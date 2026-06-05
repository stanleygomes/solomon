import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from loguru import logger
from peewee import SqliteDatabase
from core.utils.disk import DiskUtils
from core.exceptions.DatabaseError import DatabaseError


class DatabaseSetup:
  """
  Manages connections and transactions with the SQLite database.
  """

  def __init__(self, db_path: Path) -> None:
    self.db_path = db_path
    DiskUtils.ensure_directory(self.db_path.parent)
    self.db = SqliteDatabase(str(self.db_path), pragmas={"foreign_keys": 1})

  @contextmanager
  def connection(self) -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager for safe SQLite transactions.
    Automatically commits on success or rolls back if an exception occurs.
    """
    conn = sqlite3.connect(self.db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    logger.debug("🔌 Database connection established successfully at {}", self.db_path)

    try:
      yield conn
      conn.commit()
    except Exception as e:
      conn.rollback()
      raise DatabaseError("Database connection or transaction failed") from e
    finally:
      conn.close()
