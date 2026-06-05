from core.database.setup import DatabaseSetup
from core.database.models.message import MessageModel
from core.database.models.conversation import ConversationModel
from core.constants.message_role import MessageRole
from core.utils.date import DateManager


class MessageRepository:
  """
  Repository for managing MessageModel records in SQLite using Peewee.
  """

  def __init__(self, db_manager: DatabaseSetup) -> None:
    self.db_manager = db_manager
    self.db_manager.db.bind([MessageModel, ConversationModel])

  def create(
    self, conversation_id: str, role: MessageRole, content: str
  ) -> MessageModel:
    """
    Creates and returns a new message record linked to a conversation.
    """
    return MessageModel.create(
      conversation=conversation_id,
      role=role.value,
      content=content,
      created_at=DateManager.now_iso(),
    )
