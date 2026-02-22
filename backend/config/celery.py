import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('health_monitoring')

# Load config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks
app.autodiscover_tasks()

# Periodic tasks
app.conf.beat_schedule = {
    'generate-daily-tips': {
        'task': 'analytics.tasks.generate_daily_health_tips',
        'schedule': crontab(hour=8, minute=0),  # Every day at 8 AM
    },
    'calculate-diabetes-risk': {
        'task': 'analytics.tasks.calculate_diabetes_risk_batch',
        'schedule': crontab(day_of_week=1, hour=9, minute=0),  # Every Monday at 9 AM
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')