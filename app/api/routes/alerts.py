from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...database import get_db
from ...models import AlertRule, AlertEvent
from ...schemas import AlertRuleCreate, AlertRuleOut, AlertEventOut

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/rules", response_model=List[AlertRuleOut])
def list_rules(db: Session = Depends(get_db)):
    return db.query(AlertRule).order_by(AlertRule.id.asc()).all()


@router.post("/rules", response_model=AlertRuleOut)
def create_rule(body: AlertRuleCreate, db: Session = Depends(get_db)):
    if db.query(AlertRule).filter(AlertRule.name == body.name).first():
        raise HTTPException(status_code=400, detail="Rule with this name already exists")
    rule = AlertRule(
        name=body.name,
        level=body.level,
        threshold_count=body.threshold_count,
        window_minutes=body.window_minutes,
        enabled=body.enabled,
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


@router.get("/events", response_model=List[AlertEventOut])
def list_events(minutes: int = 1440, db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(minutes=max(1, minutes))
    return (
        db.query(AlertEvent)
        .filter(AlertEvent.triggered_at >= since)
        .order_by(AlertEvent.triggered_at.desc())
        .all()
    )

