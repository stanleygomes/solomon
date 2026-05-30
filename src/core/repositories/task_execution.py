from peewee import fn
from core.database import DatabaseManager
from core.models.task_execution import TaskExecutionModel
from core.constants.execution_status import ExecutionStatus


class TaskExecutionRepository:
  """
  Repository for managing TaskExecution records in the SQLite database using Peewee.
  """

  def __init__(self, db_manager: DatabaseManager) -> None:
    self.db_manager = db_manager
    self.db_manager.db.bind([TaskExecutionModel])

  def save(self, task_name: str, status: ExecutionStatus, executed_at: str) -> None:
    """
    Saves a TaskExecution record to the database using Peewee.
    """
    TaskExecutionModel.create(
      task_name=task_name,
      status=status,
      executed_at=executed_at,
    )

  def has_run_on_date(self, task_name: str, target_date: str) -> bool:
    """
    Checks if the specified task has executed successfully on the given date (YYYY-MM-DD) using Peewee.
    """
    query = TaskExecutionModel.select().where(
      (TaskExecutionModel.task_name == task_name)
      & (TaskExecutionModel.status == ExecutionStatus.SUCCESS)
      & (fn.date(TaskExecutionModel.executed_at) == target_date)
    )
    return query.exists()
