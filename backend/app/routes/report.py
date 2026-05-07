from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportOut

router = APIRouter(prefix="/report", tags=["Reports"])


@router.post("/submit", response_model=ReportOut)
def submit_report(payload: ReportCreate, db: Session = Depends(get_db)) -> Report:
    report = Report(
        disease_predicted=payload.disease_predicted,
        confidence=payload.confidence,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

