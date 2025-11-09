from datetime import timedelta
from celery import shared_task
from sqlalchemy.orm import Session

from ..database import session_scope
from ..services.log_processor import persist_log
from ..services.analytics import counts_by_level
from ..services.alerting import evaluate_rules


@shared_task(name="app.celery_app.tasks.process_log_task")
def process_log_task(log: dict) -> int:
    with session_scope() as session:  # type: Session
        entry = persist_log(session, log)
        session.flush()
        evaluate_rules(session, entry)
        session.flush()
        return entry.id


@shared_task(name="app.celery_app.tasks.compute_analytics_task")
def compute_analytics_task(window_minutes: int = 60) -> dict:
    with session_scope() as session:  # type: Session
        data = counts_by_level(session, timedelta(minutes=window_minutes))
        return data

