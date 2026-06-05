from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.constants.app import APP_NAME, APP_VERSION
from core.config.environment import Config
from core.config.logger import setup_logger
from core.database.setup import DatabaseSetup
from core.database.migrator import DatabaseMigrator
from core.utils.disk import DiskManager
from api.routes.status import router as status_router


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
app.include_router(status_router)
