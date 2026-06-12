from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps.auth import get_current_user, get_current_user_optional
from app.models.report import Report
from app.models.user import User
from app.schemas.report import ReportCreate, ReportHistoryOut, ReportOut
from app.services.cluster_service import check_clusters_after_report
from app.services.device_service import upsert_user_location
from app.services.fcm_service import notify_cluster_alert

router = APIRouter(prefix="/report", tags=["Reports"])


def _cluster_message(clusters) -> str | None:
    if not clusters:
        return None
    top = max(clusters, key=lambda c: c.case_count)
    return (
        f"Outbreak cluster detected: {top.case_count} {top.disease} cases nearby "
        f"({top.severity} severity). Stay alert."
    )


@router.post("/submit", response_model=ReportOut)
def submit_report(
    payload: ReportCreate,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
) -> dict:
    report = Report(
        user_id=user.id if user else None,
        disease_predicted=payload.disease_predicted,
        confidence=payload.confidence,
        latitude=payload.latitude,
        longitude=payload.longitude,
        risk_score=payload.risk_score,
        risk_tier=payload.risk_tier,
        source=payload.source,
        exposure_summary=payload.exposure_summary,
        symptoms_reported=payload.symptoms_reported,
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    if payload.device_token:
        upsert_user_location(
            db,
            device_token=payload.device_token.strip(),
            latitude=payload.latitude,
            longitude=payload.longitude,
            user=user,
        )

    triggered, new_alerts = check_clusters_after_report(db, report)
    for alert in new_alerts:
        notify_cluster_alert(db, alert)

    out = ReportOut.model_validate(report)
    return out.model_copy(update={"cluster_alert": _cluster_message(triggered)})


@router.get("/history", response_model=ReportHistoryOut)
def report_history(
    limit: int = 50,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    total = db.scalar(select(func.count()).select_from(Report).where(Report.user_id == user.id)) or 0
    rows = db.scalars(
        select(Report)
        .where(Report.user_id == user.id)
        .order_by(Report.timestamp.desc())
        .limit(min(limit, 100))
    ).all()
    return {
        "reports": [ReportOut.model_validate(r) for r in rows],
        "total": total,
    }
