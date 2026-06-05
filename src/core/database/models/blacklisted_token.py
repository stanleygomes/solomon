from peewee import CharField, Model


class BlacklistedTokenModel(Model):
  """
  Peewee Model representing the blacklisted_tokens table (DB fallback).
  """

  token = CharField(primary_key=True)
  blacklisted_at = CharField(null=False)
  expires_at = CharField(null=False)

  class Meta:
    table_name = "blacklisted_tokens"
