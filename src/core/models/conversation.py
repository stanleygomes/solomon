import uuid
from peewee import CharField, Model, UUIDField


class ConversationModel(Model):
  """
  Peewee Model representing the conversations table.
  """

  id = UUIDField(primary_key=True, default=uuid.uuid4)
  title = CharField(null=True)
  created_at = CharField(null=False)
  updated_at = CharField(null=False)

  class Meta:
    table_name = "conversations"
