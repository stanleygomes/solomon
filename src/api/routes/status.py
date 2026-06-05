from fastapi import APIRouter
from core.constants.app import APP_NAME, APP_VERSION

router = APIRouter()


@router.get("/status")
def get_status() -> dict[str, str]:
  """
  Retrieve the current operational status of the API.
  """
  return {
    "status": "ok",
    "app": APP_NAME,
    "version": APP_VERSION,
  }
