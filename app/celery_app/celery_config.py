from celery import Celery

from ..config import settings


celery_app = Celery(
    "log_analytics",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.celery_app.tasks"],
)

celery_app.conf.timezone = "UTC"
celery_app.conf.task_acks_late = True
celery_app.conf.worker_max_tasks_per_child = 1000

# Optional: periodic tasks (e.g., compute analytics every 5 minutes)
celery_app.conf.beat_schedule = {
    # "compute-analytics": {
    #     "task": "app.celery_app.tasks.compute_analytics_task",
    #     "schedule": 300.0,
    #     "args": (60,),
    # },
}

