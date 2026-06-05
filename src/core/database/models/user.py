import uuid
from peewee import CharField, Model, UUIDField


class UserModel(Model):
  """
  Peewee Model representing the users table.
  """

  id = UUIDField(primary_key=True, default=uuid.uuid4)
  email = CharField(unique=True, null=False)
  created_at = CharField(null=False)
  updated_at = CharField(null=False)

  class Meta:
    table_name = "users"
