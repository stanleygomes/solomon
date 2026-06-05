from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.constants.app import APP_NAME, APP_VERSION
from core.config.environment import Config
from core.config.logger import setup_logger
from core.database.setup import DatabaseSetup
from core.database.migrator import DatabaseMigrator
from core.services.mail.mailer import Mailer
from core.services.auth.auth_service import AuthService
from api.routes.status import router as status_router
from api.routes.auth import router as auth_router
from api.exceptions import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
  config = Config.load()
  setup_logger(config.logger)

  db_manager = DatabaseSetup(config.db.path)
  migrator = DatabaseMigrator(db_manager)
  migrator.migrate()

  mailer = Mailer(config.mail)
  auth_service = AuthService(
    db_manager=db_manager,
    mailer=mailer,
    keys_dir=config.auth.keys_dir,
    refresh_token_expiration=config.auth.refresh_token_expiration,
    magic_code_expiration=config.auth.magic_code_expiration,
    jwt_algorithm=config.auth.jwt_algorithm,
  )

  # Expose to API state
  app.state.config = config
  app.state.db_manager = db_manager
  app.state.mailer = mailer
  app.state.auth_service = auth_service

  yield


app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)
register_exception_handlers(app)
app.include_router(status_router)
app.include_router(auth_router)
