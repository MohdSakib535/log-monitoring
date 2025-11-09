from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON

from .database import Base


class LogEntry(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)
    level = Column(String(16), index=True, nullable=False)
    message = Column(Text, nullable=False)
    service_name = Column(String(128), index=True, nullable=True)
    # 'metadata' is reserved by SQLAlchemy's Declarative API; map column name 'metadata' to attribute 'extra'.
    extra = Column("metadata", JSON, nullable=True)


class AlertRule(Base):
    __tablename__ = "alert_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, nullable=False)
    level = Column(String(16), nullable=True)  # None => any
    threshold_count = Column(Integer, nullable=False, default=10)
    window_minutes = Column(Integer, nullable=False, default=5)
    enabled = Column(Boolean, default=True, nullable=False)

    events = relationship("AlertEvent", back_populates="rule", cascade="all, delete-orphan")


class AlertEvent(Base):
    __tablename__ = "alert_events"

    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(Integer, ForeignKey("alert_rules.id"), nullable=False)
    triggered_at = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)
    count = Column(Integer, nullable=False, default=0)
    details = Column(Text, nullable=True)

    rule = relationship("AlertRule", back_populates="events")
