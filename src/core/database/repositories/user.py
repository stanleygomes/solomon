from core.database.setup import DatabaseSetup
from core.database.models.user import UserModel
from core.utils.date import DateUtils


class UserRepository:
  """
  Repository for managing UserModel records.
  """

  def __init__(self, db_manager: DatabaseSetup) -> None:
    self.db_manager = db_manager
    self.db_manager.db.bind([UserModel])

  def create(self, email: str) -> UserModel:
    """
    Creates a new user.
    """
    now = DateUtils.now_iso()
    return UserModel.create(email=email, created_at=now, updated_at=now)

  def find_by_email(self, email: str) -> UserModel | None:
    """
    Finds a user by email address.
    """
    return UserModel.filter(UserModel.email == email).first()

  def find_by_id(self, user_id: str) -> UserModel | None:
    """
    Finds a user by ID.
    """
    return UserModel.filter(UserModel.id == user_id).first()
