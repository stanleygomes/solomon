import sys
from loguru import logger
from core.config.environment import Config
from core.database.setup import DatabaseSetup
from core.database.seeders import UserSeeder, StudyClassSeeder, ConversationSeeder


def run_seeders() -> None:
  """
  Initializes configuration, database connections, and executes all database seeders.
  """
  logger.info("🌱 Starting database seeding process...")

  try:
    # 1. Load config and set up database connection
    config = Config.load()
    db_manager = DatabaseSetup(config.db.path)

    # 2. Register and execute seeders in dependency order
    seeders = [
      UserSeeder(),
      StudyClassSeeder(),
      ConversationSeeder(),
    ]

    for seeder in seeders:
      seeder.seed(db_manager)

    logger.info("✨ Database seeding completed successfully!")

  except Exception as e:
    logger.error("❌ Seeding failed with error: {}", e)
    sys.exit(1)


if __name__ == "__main__":
  run_seeders()
