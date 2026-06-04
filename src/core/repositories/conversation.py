from core.database.setup import DatabaseSetup
from core.models.conversation import ConversationModel
from core.utils.date import DateManager


class ConversationRepository:
  """
  Repository for managing ConversationModel records in SQLite using Peewee.
  """

  def __init__(self, db_manager: DatabaseSetup) -> None:
    self.db_manager = db_manager
    self.db_manager.db.bind([ConversationModel])

  def create(self, title: str | None = None) -> ConversationModel:
    """
    Creates and returns a new conversation record.
    """
    now = DateManager.now_iso()
    return ConversationModel.create(
      title=title,
      created_at=now,
      updated_at=now,
    )
