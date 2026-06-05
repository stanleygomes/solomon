from core.database.setup import DatabaseSetup
from core.database.models.blacklisted_token import BlacklistedTokenModel
from core.utils.date import DateManager


class BlacklistedTokenRepository:
  """
  Repository for managing BlacklistedTokenModel records.
  """

  def __init__(self, db_manager: DatabaseSetup) -> None:
    self.db_manager = db_manager
    self.db_manager.db.bind([BlacklistedTokenModel])

  def blacklist(self, token: str, expires_at: str) -> BlacklistedTokenModel:
    """
    Saves a token to the blacklist.
    """
    now = DateManager.now_iso()
    return BlacklistedTokenModel.create(
      token=token,
      blacklisted_at=now,
      expires_at=expires_at,
    )

  def is_blacklisted(self, token: str) -> bool:
    """
    Checks if a token is in the blacklist.
    """
    return BlacklistedTokenModel.filter(BlacklistedTokenModel.token == token).exists()

  def cleanup_expired(self) -> None:
    """
    Deletes all expired blacklisted tokens.
    """
    now = DateManager.now_iso()
    BlacklistedTokenModel.delete().where(
      BlacklistedTokenModel.expires_at < now
    ).execute()
