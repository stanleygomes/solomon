import uuid
from peewee import CharField, ForeignKeyField, Model, TextField, UUIDField
from core.models.conversation import ConversationModel


class MessageModel(Model):
  """
  Peewee Model representing the messages table.
  """

  id = UUIDField(primary_key=True, default=uuid.uuid4)
  conversation = ForeignKeyField(
    ConversationModel,
    backref="messages",
    column_name="conversation_id",
    on_delete="CASCADE",
  )
  role = CharField(null=False)
  content = TextField(null=False)
  created_at = CharField(null=False)

  class Meta:
    table_name = "messages"
