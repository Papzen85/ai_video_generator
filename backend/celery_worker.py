# backend/celery_app.py
from celery import Celery
import os

# Use Render environment variable for Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery(
    "backend",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery.conf.task_routes = {
    "backend.tasks.*": {"queue": "default"},
}
