import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...database import get_db
from ...models import LogEntry
from ...schemas import LogIngest, LogOut
from ...config import settings
from ...celery_app.tasks import process_log_task

router = APIRouter(prefix="/logs", tags=["logs"])


def _produce_to_kafka(payload: dict) -> bool:
    try:
        from ...kafka.producer import get_producer

        producer = get_producer()
        producer.produce(payload)
        return True
    except Exception:
        return False


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
def ingest_log(body: LogIngest):
    data = body.dict()
    # Prefer Kafka; fall back to Celery direct/local apply for testing
    produced = _produce_to_kafka(data)
    if not produced:
        if settings.APP_ENV == "testing":
            # Local apply when testing to avoid broker deps
            process_log_task.s(data).apply()
        else:
            process_log_task.delay(data)
    return {"status": "queued", "via": "kafka" if produced else "celery"}


@router.get("/", response_model=List[LogOut])
def list_logs(limit: int = 50, db: Session = Depends(get_db)):
    logs = db.query(LogEntry).order_by(LogEntry.id.desc()).limit(limit).all()
    return list(reversed(logs))

