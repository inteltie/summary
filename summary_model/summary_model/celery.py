import os
import time
import subprocess
from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_init
import logging


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'summary_model.settings')

app = Celery('summary_model')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()