import tomllib
from pathlib import Path
from typing import Any

CONFIG_PATH = Path("storage/config.toml")


def load_cli_config() -> dict[str, Any]:
  """
  Load the CLI configuration from storage/config.toml.
  """
  if not CONFIG_PATH.exists():
    return {}
  try:
    with open(CONFIG_PATH, "rb") as f:
      return tomllib.load(f)
  except Exception:
    return {}


def get_api_host() -> str:
  """
  Get the configured API host, defaulting to local host if not set.
  """
  config = load_cli_config()
  api_config = config.get("api", {})
  if isinstance(api_config, dict):
    return api_config.get("host", "http://127.0.0.1:7000")
  return "http://127.0.0.1:7000"


def save_api_host(host: str) -> None:
  """
  Save the API host configuration to storage/config.toml.
  """
  CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
  config = load_cli_config()

  if not isinstance(config.get("api"), dict):
    config["api"] = {}

  config["api"]["host"] = host

  # Write back to TOML formatted file
  lines = []
  for section, values in config.items():
    if isinstance(values, dict):
      lines.append(f"[{section}]")
      for key, val in values.items():
        if isinstance(val, str):
          lines.append(f'{key} = "{val}"')
        else:
          lines.append(f"{key} = {val}")
      lines.append("")

  with open(CONFIG_PATH, "w") as f:
    f.write("\n".join(lines))
