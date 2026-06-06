import time
from collections import defaultdict
from dataclasses import dataclass
from typing import Any
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


@dataclass(frozen=True)
class RateLimitConfig:
  requests_limit: int
  window_seconds: int


class RateLimitMiddleware(BaseHTTPMiddleware):
  """
  In-memory fixed-window rate limiter middleware.
  """

  def __init__(
    self,
    app: Any,
    requests_limit: int,
    window_seconds: int,
  ) -> None:
    super().__init__(app)
    self.requests_limit = requests_limit
    self.window_seconds = window_seconds
    self.client_records: dict[str, list[float]] = defaultdict(list)

  async def dispatch(
    self, request: Request, call_next: RequestResponseEndpoint
  ) -> Response:
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()

    # Clean up old timestamps outside the window
    timestamps = self.client_records[client_ip]
    self.client_records[client_ip] = [
      ts for ts in timestamps if now - ts < self.window_seconds
    ]

    # Check limit
    if len(self.client_records[client_ip]) >= self.requests_limit:
      return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Too many requests. Please try again later."},
      )

    # Record current request
    self.client_records[client_ip].append(now)

    return await call_next(request)
