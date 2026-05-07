from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.disease import Disease
from app.models.report import Report
from app.models.transmission_route import TransmissionRoute
from app.schemas.risk import ExposureInput


def _category(score: float) -> str:
    if score < 20:
        return "Low"
    if score < 50:
        return "Moderate"
    if score < 80:
        return "High"
    return "Critical"


def calculate_human_risk(db: Session, payload: ExposureInput) -> dict:
    report = None
    if payload.report_id is not None:
        report = db.get(Report, payload.report_id)
    if report is None:
        report = db.scalar(select(Report).order_by(Report.timestamp.desc()))
    if report is None:
        raise ValueError("No disease report found. Submit a report first.")

    disease = db.scalar(select(Disease).where(Disease.name.ilike(report.disease_predicted)))
    if disease is None:
        raise ValueError(f"Disease '{report.disease_predicted}' is not present in database.")

    routes = db.scalars(select(TransmissionRoute).where(TransmissionRoute.disease_id == disease.id)).all()
    if not routes:
        raise ValueError(f"No transmission routes configured for disease '{disease.name}'.")

    # Placeholder Bayesian-like weighted risk, driven by DB probabilities.
    primary_route = max(routes, key=lambda r: r.base_probability)
    base = float(primary_route.base_probability)
    modifiers = [
        0.16 if payload.direct_contact_without_gloves else 0.0,
        0.18 if payload.consumed_raw_milk_or_meat else 0.0,
        0.14 if payload.has_open_wounds else 0.0,
        0.08 if payload.children_in_contact else 0.0,
        0.10 if payload.elderly_or_pregnant_in_contact else 0.0,
        -0.12 if payload.vaccinated_against_relevant_disease else 0.06,
    ]
    probability = max(0.0, min(1.0, base + sum(modifiers)))
    score = round(probability * 100, 2)

    return {
        "disease": disease.name,
        "score": score,
        "category": _category(score),
        "route_used": primary_route.route,
        "report_id": report.id,
    }

