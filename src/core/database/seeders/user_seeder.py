from core.database.seeders.base import BaseSeeder
from core.database.setup import DatabaseSetup
from core.database.models.user import UserModel
from core.utils.date import DateUtils
from loguru import logger


class UserSeeder(BaseSeeder):
  """
  Seeder for the users table.
  """

  def seed(self, db_manager: DatabaseSetup) -> None:
    db_manager.db.bind([UserModel])

    users_data = [
      {"email": "solomon@admin.local"},
    ]

    logger.info("👥 Seeding users...")
    for user_info in users_data:
      user, created = UserModel.get_or_create(
        email=user_info["email"],
        defaults={
          "created_at": DateUtils.now_iso(),
          "updated_at": DateUtils.now_iso(),
        },
      )
      if created:
        logger.debug("✅ Created user: {}", user.email)
      else:
        logger.debug("⏭️ User already exists: {}", user.email)
