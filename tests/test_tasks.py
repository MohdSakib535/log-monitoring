import os
os.environ["APP_ENV"] = "testing"

from app.celery_app.tasks import compute_analytics_task


def test_compute_analytics_task_runs():
    # Should return a dict even if DB is empty
    result = compute_analytics_task.apply(args=(5,)).get()
    assert isinstance(result, dict)
