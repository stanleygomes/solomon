import uuid
from peewee import CharField, IntegerField, Model, UUIDField


class MagicCodeModel(Model):
  """
  Peewee Model representing the magic_codes table (used as DB fallback/audit trail).
  """

  id = UUIDField(primary_key=True, default=uuid.uuid4)
  email = CharField(null=False)
  code = CharField(null=False)
  attempts = IntegerField(default=0)
  expires_at = CharField(null=False)
  created_at = CharField(null=False)

  class Meta:
    table_name = "magic_codes"
