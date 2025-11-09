from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy.orm import Session

from ..models import LogEntry


def persist_log(session: Session, log: Dict[str, Any]) -> LogEntry:
    entry = LogEntry(
        level=log.get("level", "INFO"),
        message=log.get("message", ""),
        service_name=log.get("service_name"),
        extra=log.get("metadata"),
    )
    session.add(entry)
    session.flush()
    return entry
