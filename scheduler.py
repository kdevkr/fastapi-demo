import datetime
import logging

from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from settings import settings

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler(jobstores={'default': MemoryJobStore()},
                             timezone=settings.timezone)


@scheduler.scheduled_job('interval', seconds=1)
async def example():
    logger.info("run example at {0}".format(datetime.datetime.now()))
