from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from core.exceptions.SolomonError import SolomonError
from core.exceptions.PreconditionFailedError import PreconditionFailedError
from core.exceptions.NotFoundError import NotFoundError
from core.exceptions.ValidationError import ValidationError
from core.exceptions.DatabaseError import DatabaseError
from core.exceptions.ExternalServiceError import ExternalServiceError


def register_exception_handlers(app: FastAPI) -> None:
  """
  Registers global exception handlers to map domain exceptions to HTTP responses.
  """

  @app.exception_handler(PreconditionFailedError)
  async def precondition_failed_handler(
    request: Request, exc: PreconditionFailedError
  ) -> JSONResponse:
    return JSONResponse(
      status_code=status.HTTP_400_BAD_REQUEST,
      content={"detail": str(exc)},
    )

  @app.exception_handler(ValidationError)
  async def validation_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
      status_code=status.HTTP_400_BAD_REQUEST,
      content={"detail": str(exc)},
    )

  @app.exception_handler(NotFoundError)
  async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
      status_code=status.HTTP_404_NOT_FOUND,
      content={"detail": str(exc)},
    )

  @app.exception_handler(ExternalServiceError)
  async def external_service_handler(
    request: Request, exc: ExternalServiceError
  ) -> JSONResponse:
    return JSONResponse(
      status_code=status.HTTP_502_BAD_GATEWAY,
      content={"detail": str(exc)},
    )

  @app.exception_handler(DatabaseError)
  async def database_handler(request: Request, exc: DatabaseError) -> JSONResponse:
    return JSONResponse(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      content={"detail": f"Erro de banco de dados: {str(exc)}"},
    )

  @app.exception_handler(SolomonError)
  async def generic_solomon_handler(
    request: Request, exc: SolomonError
  ) -> JSONResponse:
    return JSONResponse(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      content={"detail": f"Erro interno do servidor: {str(exc)}"},
    )
