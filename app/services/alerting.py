from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models import AlertRule, AlertEvent, LogEntry

print("hekk sakib")
def _count_logs(session: Session, since: datetime, level: Optional[str]) -> int:
    q = session.query(func.count(LogEntry.id)).filter(LogEntry.timestamp >= since)
    if level:
        q = q.filter(LogEntry.level == level)
    return int(q.scalar() or 0)


def evaluate_rules(session: Session, entry: LogEntry) -> None:
    now = datetime.utcnow()
    rules = (
        session.query(AlertRule)
        .filter(AlertRule.enabled == True)  # noqa: E712
        .all()
    )
    for rule in rules:
        if rule.level and rule.level != entry.level:
            continue
        since = now - timedelta(minutes=rule.window_minutes)
        count = _count_logs(session, since, rule.level)
        if count >= rule.threshold_count:
            event = AlertEvent(
                rule_id=rule.id,
                triggered_at=now,
                count=count,
                details=f"Threshold {rule.threshold_count} in {rule.window_minutes}m reached for level={rule.level or 'ANY'}",
            )
            session.add(event)
            session.flush()

