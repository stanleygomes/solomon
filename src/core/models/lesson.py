import uuid
from peewee import CharField, ForeignKeyField, IntegerField, Model, TextField, UUIDField
from core.models.study_class import StudyClassModel


class LessonModel(Model):
  """
  Peewee Model representing the lessons table.
  """

  id = UUIDField(primary_key=True, default=uuid.uuid4)
  class_plan = ForeignKeyField(
    StudyClassModel,
    backref="lessons",
    column_name="class_id",
    on_delete="CASCADE",
  )
  day_number = IntegerField(null=False)
  topic = CharField(null=False)
  summary = TextField(null=True)
  status = CharField(null=False, default="PENDING")

  class Meta:
    table_name = "lessons"
