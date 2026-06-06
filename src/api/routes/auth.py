from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.schemas.auth import (
  EmailRequestSchema,
  VerifyRequestSchema,
  TokenResponseSchema,
  MessageResponseSchema,
)
from core.services.auth.auth_service import AuthService
from core.exceptions.UnauthorizedError import UnauthorizedError

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer(auto_error=False)


def get_auth_service(request: Request) -> AuthService:
  """
  Dependency injection to retrieve the AuthService instance from app state.
  """
  return request.app.state.container.auth_service


@router.post(
  "/magic-code",
  response_model=MessageResponseSchema,
  status_code=status.HTTP_200_OK,
  summary="Request a passwordless magic code",
)
def request_magic_code(
  payload: EmailRequestSchema,
  auth_service: AuthService = Depends(get_auth_service),
):
  """
  Generates and emails a 6-digit verification code to the user.
  """
  auth_service.request_magic_code(payload.email)
  return MessageResponseSchema(message="Temporary code sent to your email")


@router.post(
  "/verify",
  response_model=TokenResponseSchema,
  status_code=status.HTTP_200_OK,
  summary="Verify magic code and receive JWT session tokens",
)
def verify_magic_code(
  payload: VerifyRequestSchema,
  request: Request,
  response: Response,
  auth_service: AuthService = Depends(get_auth_service),
):
  """
  Verifies the magic code. If valid, issues access and refresh tokens.
  The refresh token is stored in a secure HttpOnly cookie.
  """
  auth_service.verify_magic_code(payload.email, payload.code)
  tokens = auth_service.issue_tokens(payload.email)

  response.set_cookie(
    key="refresh_token",
    value=tokens.refresh_token,
    httponly=True,
    secure=request.app.state.container.config.auth.cookie_secure,
    samesite="lax",
    max_age=request.app.state.container.config.auth.refresh_token_expiration,
  )

  return TokenResponseSchema(access_token=tokens.access_token)


@router.post(
  "/refresh",
  response_model=TokenResponseSchema,
  status_code=status.HTTP_200_OK,
  summary="Refresh short-lived access token using long-lived refresh token cookie",
)
def refresh_session(
  request: Request,
  response: Response,
  auth_service: AuthService = Depends(get_auth_service),
):
  """
  Refreshes the session using the HttpOnly cookie's refresh token.
  The old refresh token gets revoked/blacklisted.
  """
  refresh_token = request.cookies.get("refresh_token")

  if not refresh_token:
    raise UnauthorizedError("Token de atualização ausente")

  tokens = auth_service.refresh_tokens(refresh_token)

  response.set_cookie(
    key="refresh_token",
    value=tokens.refresh_token,
    httponly=True,
    secure=request.app.state.container.config.auth.cookie_secure,
    samesite="lax",
    max_age=request.app.state.container.config.auth.refresh_token_expiration,
  )

  return TokenResponseSchema(access_token=tokens.access_token)


@router.post(
  "/logout",
  response_model=MessageResponseSchema,
  status_code=status.HTTP_200_OK,
  summary="Logout user session and blacklist active tokens",
)
def logout(
  request: Request,
  response: Response,
  credentials: HTTPAuthorizationCredentials | None = Depends(security),
  auth_service: AuthService = Depends(get_auth_service),
):
  """
  Logs the user out by blacklisting the access token and deleting the refresh token cookie.
  """
  # Blacklist access token if provided
  if credentials and credentials.credentials:
    auth_service.blacklist_token(credentials.credentials)

  # Blacklist refresh token if provided
  refresh_token = request.cookies.get("refresh_token")

  if refresh_token:
    auth_service.blacklist_token(refresh_token)

  # Delete refresh token cookie
  response.delete_cookie("refresh_token")

  return MessageResponseSchema(message="Sessão encerrada com sucesso")
