import argparse
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

from core.logger import Logger
from core.config import load_config
from core.state import load_state
from scheduler.engine import Scheduler


def get_base_dir() -> Path:
  # If config.json exists in CWD, use it
  if Path("config.json").exists():
    return Path.cwd()

  # Otherwise fallback to the script's directory
  return Path(__file__).parent.absolute()


def main():
  load_dotenv()
  parser = argparse.ArgumentParser(
    description="Solomon Cron Coordinator (Python Version)"
  )
  parser.add_argument(
    "--config", type=str, help="Path to the configuration file (config.json)"
  )
  parser.add_argument(
    "--state", type=str, help="Path to the execution state file (state.json)"
  )
  parser.add_argument("--logs", type=str, help="Path to the logs directory")
  parser.add_argument(
    "--run-task", type=str, help="Force-run a specific task by ID immediately"
  )

  args = parser.parse_args()

  base_dir = get_base_dir()

  config_path = args.config or str(base_dir / "config.json")
  state_path = (
    args.state or os.getenv("STATE_PATH") or str(base_dir / "temp" / "state.json")
  )
  logs_dir = args.logs or os.getenv("LOGS_DIR") or str(base_dir / "temp" / "logs")

  # 1. Initialize Logger
  try:
    logger = Logger(logs_dir)
  except Exception as e:
    print(f"FATAL: Failed to initialize logger: {e}", file=sys.stderr)
    sys.exit(1)

  logger.log("Initializing Solomon Cron Coordinator (Python)")
  logger.log("Base Directory: %s", str(base_dir))
  logger.log("Config Path:    %s", config_path)
  logger.log("State Path:     %s", state_path)
  logger.log("Logs Directory: %s", logs_dir)

  # 2. Load Config
  try:
    cfg = load_config(config_path)
  except Exception as e:
    logger.log("FATAL: Failed to load configuration: %s", str(e))
    sys.exit(1)

  # 3. Load State
  try:
    st = load_state(state_path)
  except Exception as e:
    logger.log("FATAL: Failed to load execution state: %s", str(e))
    sys.exit(1)

  # 4. Run Scheduler
  scheduler = Scheduler(cfg, st, state_path, logger)

  if args.run_task:
    try:
      scheduler.force_run_task(args.run_task)
      sys.exit(0)
    except Exception:
      # Error already logged by scheduler
      sys.exit(1)

  try:
    scheduler.run()
  except Exception as e:
    logger.log("FATAL: Scheduler execution failed: %s", str(e))
    sys.exit(1)


if __name__ == "__main__":
  main()
