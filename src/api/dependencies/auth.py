from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.services.auth.auth_service import AuthService
from core.exceptions.UnauthorizedError import UnauthorizedError

security = HTTPBearer(auto_error=False)


def get_auth_service(request: Request) -> AuthService:
  """
  Dependency injection to retrieve the AuthService instance from the application state.
  """
  return request.app.state.container.auth_service


def verify_access_token(
  credentials: HTTPAuthorizationCredentials | None = Depends(security),
  auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, object]:
  """
  Dependency injection to authenticate requests using a Bearer access token.
  """
  if not credentials or not credentials.credentials:
    raise UnauthorizedError("Access token is missing or invalid")
  return auth_service.validate_access_token(credentials.credentials)
