import uuid
from peewee import CharField, ForeignKeyField, Model, UUIDField
from core.database.models.user import UserModel


class ConversationModel(Model):
  """
  Peewee Model representing the conversations table.
  """

  id = UUIDField(primary_key=True, default=uuid.uuid4)
  user = ForeignKeyField(
    UserModel,
    backref="conversations",
    column_name="user_id",
    null=True,
    on_delete="CASCADE",
  )
  title = CharField(null=True)
  created_at = CharField(null=False)
  updated_at = CharField(null=False)

  class Meta:
    table_name = "conversations"
