import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple, Optional

from core.config import Config, TaskConfig
from core.state import State, save_state
from core.logger import Logger
from core.ai import get_ai_provider
from services.daily_bread import DailyBreadService


class Scheduler:
  def __init__(
    self, config: Config, state: State, state_path: str, logger: Logger
  ) -> None:
    self.config = config
    self.state = state
    self.state_path = state_path
    self.logger = logger

  def run(self) -> None:
    self.logger.log("=== Scheduler Execution Started ===")
    now = datetime.now()
    state_changed = False

    for task in self.config.tasks:
      last_run_str = self.state.last_runs.get(task.id)
      last_run = datetime.fromisoformat(last_run_str) if last_run_str else None

      should, reason = self._should_run(task.schedule, last_run, now)

      if not should:
        self.logger.log("SKIP [%s]: %s", task.id, reason)
        continue

      self.logger.log("EXECUTE [%s]: Running task (Reason: %s)", task.id, reason)

      try:
        self._run_task(task)
        self.logger.log("SUCCESS [%s]: Task completed successfully", task.id)
        self.state.last_runs[task.id] = datetime.now().isoformat()
        state_changed = True
      except Exception as e:
        self.logger.log("ERROR [%s]: Task execution failed: %s", task.id, str(e))

    if state_changed:
      save_state(self.state_path, self.state)
      self.logger.log("State saved successfully to %s", self.state_path)

    self.logger.log("=== Scheduler Execution Finished ===")

  def force_run_task(
    self, task_id: str, template_override: Optional[str] = None
  ) -> None:
    self.logger.log("=== Force-Running Task %s ===", task_id)

    target_task = next((t for t in self.config.tasks if t.id == task_id), None)
    if not target_task:
      raise ValueError(f"Task ID '{task_id}' not found in config")

    try:
      self._run_task(target_task, template_override)
      self.logger.log("SUCCESS [%s]: Task completed successfully", task_id)
    except Exception as e:
      self.logger.log("ERROR [%s]: Task execution failed: %s", task_id, str(e))
      raise

  def _should_run(
    self, schedule: str, last_run: Optional[datetime], now: datetime
  ) -> Tuple[bool, str]:
    if not last_run:
      return True, "Task has never run before"

    if schedule == "daily":
      if last_run.date() != now.date():
        return True, "Last run was on a different day"
      return False, f"Already ran today at {last_run.strftime('%H:%M:%S')}"

    if schedule == "hourly":
      if (last_run.date() != now.date()) or (last_run.hour != now.hour):
        return True, "Last run was in a different hour"
      return False, f"Already ran this hour at {last_run.strftime('%H:%M:%S')}"

    # Parse duration (e.g., 12h, 30m)
    try:
      duration = self._parse_duration(schedule)
      elapsed = now - last_run
      if elapsed >= duration:
        return (
          True,
          f"Interval of {schedule} exceeded (elapsed: {str(elapsed).split('.')[0]})",
        )

      remaining = duration - elapsed
      return (
        False,
        f"Interval of {schedule} not met (remaining: {str(remaining).split('.')[0]})",
      )
    except ValueError as e:
      return False, f"Invalid schedule: {str(e)}"

  def _parse_duration(self, duration_str: str) -> timedelta:
    unit = duration_str[-1].lower()
    value = int(duration_str[:-1])

    if unit == "h":
      return timedelta(hours=value)
    elif unit == "m":
      return timedelta(minutes=value)
    elif unit == "s":
      return timedelta(seconds=value)
    else:
      raise ValueError(f"Unknown duration unit: {unit}")

  def _run_task(
    self, task: TaskConfig, template_override: Optional[str] = None
  ) -> None:
    if task.command.startswith("internal:"):
      self._run_internal_service(task, template_override)
      return

    # External command
    cwd = Path(task.dir).absolute() if task.dir else None

    result = subprocess.run(
      [task.command] + task.args, cwd=cwd, capture_output=True, text=True
    )

    if result.stdout or result.stderr:
      combined_output = (result.stdout + "\n" + result.stderr).encode("utf-8")
      self.logger.log_task_output(task.id, combined_output)

    if result.returncode != 0:
      raise RuntimeError(f"Command returned non-zero exit code: {result.returncode}")

  def _run_internal_service(
    self, task: TaskConfig, template_override: Optional[str] = None
  ) -> None:
    service_name = task.command.replace("internal:", "")

    if service_name == "daily-bread":
      # Check task args if no override provided
      if not template_override:
        for i, arg in enumerate(task.args):
          if arg in ["-template", "-t"] and i + 1 < len(task.args):
            template_override = task.args[i + 1]
            break

      assets_dir = Path("assets").absolute()
      db_service = DailyBreadService(self.logger, str(assets_dir))
      ai_provider = get_ai_provider()

      if template_override:
        db_service.run(ai_provider, template_name=template_override)
      else:
        db_service.run(ai_provider)
    else:
      raise ValueError(f"Unknown internal service: {service_name}")
