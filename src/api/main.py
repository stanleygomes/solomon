from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.constants.app import APP_NAME, APP_VERSION
from core.config.environment import Config
from core.config.logger import setup_logger
from core.container import Container
from api.routes.status.status import router as status_router
from api.routes.auth.auth import router as auth_router
from api.routes.chat.chat import router as chat_router
from api.exceptions import register_exception_handlers
from api.middlewares.rate_limit import RateLimitMiddleware


config = Config.load()


@asynccontextmanager
async def lifespan(app: FastAPI):
  setup_logger(config.logger)

  container = Container(config)
  container.wire()

  # Expose to API state
  app.state.container = container

  yield


app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)
register_exception_handlers(app)
app.add_middleware(
  RateLimitMiddleware,
  requests_limit=config.rate_limit.requests_limit,
  window_seconds=config.rate_limit.window_seconds,
)
app.include_router(status_router)
app.include_router(auth_router)
app.include_router(chat_router)
