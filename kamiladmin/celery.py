from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


# Nastavení Django konfigurace pro Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kamiladmin.settings')

celery_app = Celery('kamiladmin')

# Načtení konfigurace z Django settings
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatické načítání úloh (tasks) ze všech aplikací
celery_app.autodiscover_tasks()


celery_app.conf.beat_schedule = {
    'send_work_anniversary_email_daily': {
        'task': 'viewer.task.send_work_anniversary_email',
        'schedule': crontab(minute=15, hour=22),  # Běží každý den v 18:00
    },
}
