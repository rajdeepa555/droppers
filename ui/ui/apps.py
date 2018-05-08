# App configuration

from datetime import datetime
from datetime import timedelta

import dateutil.relativedelta as REL

from django.apps import AppConfig
from django.conf import settings
from .views import justForTest
import django_rq


class EbayConfig(AppConfig):
    name = 'ebayautomation'
    verbose_name = 'ebayautomation'

    def ready(self):
        print("ready is called")
        # if not settings.DEBUG:

        # from youtube.tasks import update_metadata, update_analytics
        # from youtube.tasks import bulk_report, compare_analytics

        # Get default scheduler
        self.scheduler = django_rq.get_scheduler()

        # Delete any existing jobs in the scheduler when the app starts up
        for job in self.scheduler.get_jobs():
            job.delete()

        # Have 'update_metadata' run every week
        start = datetime.utcnow().replace(hour=0, minute=0) 
        # next sunday
        next_sunday = REL.relativedelta(days=1, weekday=REL.SU)
        start = start + next_sunday
        week = 60 * 60 * 24 * 7
        self.scheduler.schedule(
            start, update_metadata, interval=week, repeat=None)
        self.scheduler.schedule(
            start, compare_analytics, interval=week, repeat=None)

        # Have 'update_analytics' run every day
        start = datetime.utcnow().replace(hour=0, minute=0)
        start = start + timedelta(days=1)
        day = 60 * 60 * 24
        self.scheduler.schedule(
            start, update_analytics, interval=day, repeat=None)
        self.scheduler.schedule(
            start, bulk_report, interval=day, repeat=None)
