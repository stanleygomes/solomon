from cron.jobs.base import CronJob
from cron.jobs.daily_bread import DailyBreadJob

JOBS: list[type[CronJob]] = [
  DailyBreadJob,
]
