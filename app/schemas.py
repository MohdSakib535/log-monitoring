from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class LogIngest(BaseModel):
    level: str = Field(..., regex=r"^(DEBUG|INFO|WARN|WARNING|ERROR|CRITICAL)$")
    message: str
    service_name: Optional[str] = "default"
    metadata: Optional[Dict[str, Any]] = None


class LogOut(BaseModel):
    id: int
    timestamp: datetime
    level: str
    message: str
    service_name: Optional[str]

    class Config:
        orm_mode = True


class AnalyticsOut(BaseModel):
    window_minutes: int
    counts_by_level: Dict[str, int]
    top_services: Dict[str, int]


class AlertRuleCreate(BaseModel):
    name: str
    level: Optional[str] = None
    threshold_count: int = 10
    window_minutes: int = 5
    enabled: bool = True


class AlertRuleOut(BaseModel):
    id: int
    name: str
    level: Optional[str]
    threshold_count: int
    window_minutes: int
    enabled: bool

    class Config:
        orm_mode = True


class AlertEventOut(BaseModel):
    id: int
    rule_id: int
    triggered_at: datetime
    count: int
    details: Optional[str]

    class Config:
        orm_mode = True

