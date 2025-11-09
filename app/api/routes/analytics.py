from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...services.analytics import counts_by_level, top_services_in_window
from ...schemas import AnalyticsOut

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/", response_model=AnalyticsOut)
def get_analytics(minutes: int = 60, db: Session = Depends(get_db)):
    window = timedelta(minutes=max(1, minutes))
    counts = counts_by_level(db, window)
    top = top_services_in_window(db, window, limit=5)
    return AnalyticsOut(window_minutes=int(window.total_seconds() // 60), counts_by_level=counts, top_services=top)

