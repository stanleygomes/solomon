import uuid
from peewee import CharField, Model, UUIDField


class TaskExecutionModel(Model):
  """
  Peewee Model representing the task_executions table.
  """

  id = UUIDField(primary_key=True, default=uuid.uuid4)
  task_name = CharField(null=False)
  status = CharField(null=False)
  executed_at = CharField(null=False)

  class Meta:
    table_name = "task_executions"
