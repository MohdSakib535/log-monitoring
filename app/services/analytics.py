from collections import Counter
from datetime import datetime, timedelta
from typing import Dict
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models import LogEntry


def counts_by_level(session: Session, window: timedelta) -> Dict[str, int]:
    since = datetime.utcnow() - window
    rows = (
        session.query(LogEntry.level, func.count(LogEntry.id))
        .filter(LogEntry.timestamp >= since)
        .group_by(LogEntry.level)
        .all()
    )
    return {lvl: int(cnt) for (lvl, cnt) in rows}


def top_services_in_window(session: Session, window: timedelta, limit: int = 5) -> Dict[str, int]:
    since = datetime.utcnow() - window
    rows = (
        session.query(LogEntry.service_name, func.count(LogEntry.id))
        .filter(LogEntry.timestamp >= since)
        .group_by(LogEntry.service_name)
        .order_by(func.count(LogEntry.id).desc())
        .limit(limit)
        .all()
    )
    return {svc or "unknown": int(cnt) for (svc, cnt) in rows}

