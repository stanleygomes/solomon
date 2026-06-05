from fastapi import FastAPI
from core.constants.app import APP_NAME, APP_VERSION


app = FastAPI(title=APP_NAME, version=APP_VERSION)


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
