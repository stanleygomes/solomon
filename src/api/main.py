from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.constants.app import APP_NAME, APP_VERSION
from core.config.environment import Config
from core.config.logger import setup_logger
from core.database.setup import DatabaseSetup
from core.database.migrator import DatabaseMigrator
from core.utils.disk import DiskManager


@asynccontextmanager
async def lifespan(app: FastAPI):
  config = Config.load()
  setup_logger(config.logger)

  db_manager = DatabaseSetup(config.db.path)
  migrations_dir = DiskManager.resolve_path(__file__, "..", "core", "migrations")
  migrator = DatabaseMigrator(db_manager, migrations_dir)
  migrator.migrate()

  yield


app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)


@app.get("/status")
def get_status() -> dict[str, str]:
  """
  Retrieve the current operational status of the API.
  """
  return {
    "status": "ok",
    "app": APP_NAME,
    "version": APP_VERSION,
  }
