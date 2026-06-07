from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler
from core.config.environment import Config
from core.container import Container
from cron.jobs import JOBS


def main() -> None:
  config = Config.load()
  container = Container(config)
  container.wire()

  scheduler = BlockingScheduler()

  # Register all jobs
  for job_cls in JOBS:
    job = job_cls(container)
    job.register(scheduler)

  logger.info("⏰ Starting Solomon Cron Daemon scheduler...")
  try:
    scheduler.start()
  except KeyboardInterrupt, SystemExit:
    logger.info("👋 Shutting down Solomon Cron Daemon scheduler.")


if __name__ == "__main__":
  main()
