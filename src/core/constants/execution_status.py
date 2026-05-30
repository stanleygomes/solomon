from enum import StrEnum


class ExecutionStatus(StrEnum):
  """
  Enum representing the outcome status of a task execution run.
  """

  SUCCESS = "SUCCESS"
  FAILED = "FAILED"
