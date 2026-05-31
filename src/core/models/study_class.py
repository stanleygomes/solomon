import uuid
from peewee import CharField, IntegerField, Model, UUIDField


class StudyClassModel(Model):
  """
  Peewee Model representing the classes table.
  """

  id = UUIDField(primary_key=True, default=uuid.uuid4)
  subject = CharField(null=False)
  duration_days = IntegerField(null=False)
  current_day = IntegerField(null=False, default=1)
  status = CharField(null=False, default="ACTIVE")
  created_at = CharField(null=False)

  class Meta:
    table_name = "classes"
