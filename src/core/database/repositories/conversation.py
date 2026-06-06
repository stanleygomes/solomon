from core.database.setup import DatabaseSetup
from core.database.models.conversation import ConversationModel
from core.database.models.user import UserModel
from core.utils.date import DateUtils


class ConversationRepository:
  """
  Repository for managing ConversationModel records in SQLite using Peewee.
  """

  def __init__(self, db_manager: DatabaseSetup) -> None:
    self.db_manager = db_manager
    self.db_manager.db.bind([ConversationModel, UserModel])

  def create(self, user_id: str, title: str | None = None) -> ConversationModel:
    """
    Creates and returns a new conversation record.
    """
    now = DateUtils.now_iso()
    return ConversationModel.create(
      user=user_id,
      title=title,
      created_at=now,
      updated_at=now,
    )
