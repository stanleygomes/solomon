from infra.database.setup import DatabaseSetup
from infra.database.models.conversation import ConversationModel
from core.utils.date import DateUtils


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
    now = DateUtils.now_iso()
    return ConversationModel.create(
      title=title,
      created_at=now,
      updated_at=now,
    )
