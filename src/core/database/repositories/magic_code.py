from core.database.setup import DatabaseSetup
from core.database.models.magic_code import MagicCodeModel
from core.utils.date import DateUtils


class MagicCodeRepository:
  """
  Repository for managing MagicCodeModel records.
  """

  def __init__(self, db_manager: DatabaseSetup) -> None:
    self.db_manager = db_manager
    self.db_manager.db.bind([MagicCodeModel])

  def create(self, email: str, code: str, expires_at: str) -> MagicCodeModel:
    """
    Saves a newly generated magic code.
    """
    now = DateUtils.now_iso()
    return MagicCodeModel.create(
      email=email,
      code=code,
      attempts=0,
      expires_at=expires_at,
      created_at=now,
    )

  def find_latest(self, email: str) -> MagicCodeModel | None:
    """
    Finds the latest code for an email address.
    """
    return (
      MagicCodeModel.filter(
        MagicCodeModel.email == email
      )
      .order_by(MagicCodeModel.created_at.desc())
      .first()
    )

  def increment_attempts(self, code_id: str) -> None:
    """
    Increments validation attempts count.
    """
    MagicCodeModel.update(attempts=MagicCodeModel.attempts + 1).where(
      MagicCodeModel.id == code_id
    ).execute()

  def delete_by_email(self, email: str) -> None:
    """
    Invalidates (deletes) all codes for a specific email once verified.
    """
    MagicCodeModel.delete().where(
      MagicCodeModel.email == email
    ).execute()
