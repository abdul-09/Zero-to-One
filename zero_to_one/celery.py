from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from zero_to_one import settings
from celery.schedules import crontab, schedule


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zero_to_one.settings')


app = Celery('zero_to_one')


app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

