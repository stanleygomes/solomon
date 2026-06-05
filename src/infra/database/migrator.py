import re
from pathlib import Path
from loguru import logger
from infra.database.setup import DatabaseSetup
from core.utils.disk import DiskUtils
from core.utils.date import DateUtils


class DatabaseMigrator:
  """
  Manages and runs database migrations using plain SQL files.
  """

  def __init__(self, db_manager: DatabaseSetup, migrations_dir: Path) -> None:
    self.db_manager = db_manager
    self.migrations_dir = migrations_dir

  def migrate(self) -> None:
    """
    Scans, validates, and runs pending migrations in transaction blocks.
    """
    logger.debug("🔄 Checking database migrations in: {}", self.migrations_dir)

    # 1. Ensure migrations directory exists
    DiskUtils.ensure_directory(self.migrations_dir)

    # 2. Ensure schema_migrations table exists
    with self.db_manager.connection() as conn:
      conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            applied_at TEXT NOT NULL
        );
        """
      )

    # 3. Retrieve applied migrations
    with self.db_manager.connection() as conn:
      cursor = conn.execute("SELECT version FROM schema_migrations ORDER BY version;")
      applied_versions = {row["version"] for row in cursor.fetchall()}

    # 4. Scan and validate migration files
    migration_files = []
    pattern = re.compile(r"^(\d{4})_.+\.sql$")

    for file_path in self.migrations_dir.glob("*.sql"):
      match = pattern.match(file_path.name)
      if not match:
        logger.error("❌ Invalid migration filename pattern: {}", file_path.name)
        raise ValueError(
          f"Migration filename '{file_path.name}' does not match pattern XXXX_description.sql"
        )
      version = int(match.group(1))
      migration_files.append((version, file_path))

    # Sort migrations by version (XXXX)
    migration_files.sort(key=lambda x: x[0])

    # 5. Execute pending migrations
    for version, file_path in migration_files:
      if version in applied_versions:
        logger.debug("⏭️ Skipping already applied migration: {}", file_path.name)
        continue

      logger.info("🚀 Running migration: {}", file_path.name)
      sql_content = DiskUtils.read_text(file_path)

      # Run each migration inside a dedicated transaction block
      with self.db_manager.connection() as conn:
        try:
          conn.executescript(sql_content)
          conn.execute(
            "INSERT INTO schema_migrations (version, name, applied_at) VALUES (?, ?, ?);",
            (version, file_path.name, DateUtils.now_iso()),
          )
          logger.info("✅ Successfully applied migration: {}", file_path.name)
        except Exception as e:
          logger.error("❌ Failed to apply migration: {}. Error: {}", file_path.name, e)
          raise e
