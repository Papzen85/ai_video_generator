from celery import Celery
import os

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
celery = Celery("vidcraft_tasks", broker=redis_url, backend=redis_url)

# autodiscover tasks if needed
celery.autodiscover_tasks(['tasks'])
