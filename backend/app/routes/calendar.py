from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
import random

from fastapi import APIRouter, HTTPException

from app.ml.watch_calendar import build_calendar
from app.ml.disease_priors import HOUSEHOLD_RISK_GROUPS
from app.schemas.calendar import CalendarOut, SymptomReportRequest

router = APIRouter(prefix="/calendar", tags=["Calendar"])

BASE_PATH = Path(__file__).resolve().parents[2]
REPORTS_DIR = BASE_PATH / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


@router.get("/{disease}", response_model=CalendarOut)
def get_calendar(disease: str, exposure_date: str) -> dict:
    try:
        d = date.fromisoformat(exposure_date)
    except Exception:
        raise HTTPException(status_code=400, detail="exposure_date must be YYYY-MM-DD")
    try:
        return build_calendar(disease, d)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


def _recommended_tests(disease: str) -> list[str]:
    return {
        "Brucellosis": ["Brucella Rose Bengal Test", "ELISA", "blood culture"],
        "Leptospirosis": ["MAT (Microscopic Agglutination Test)", "PCR", "LFT"],
        "Bovine_TB": ["Mantoux test", "Chest X-ray", "Sputum culture"],
        "Anthrax": ["Blood culture", "PCR", "Skin lesion swab"],
        "Q_Fever": ["Phase II IgM/IgG ELISA", "PCR"],
        "FMD": ["Clinical diagnosis", "PCR"],
        "LSD": ["Clinical + KOH mount / fungal culture"],
        "Ringworm": ["Clinical + KOH mount / fungal culture"],
    }.get(disease, ["Clinical examination"])


def _disease_description(disease: str) -> str:
    return {
        "Brucellosis": "A bacterial infection often linked to raw dairy and birth fluids.",
        "Leptospirosis": "A bacterial infection linked to urine-contaminated water/soil exposure.",
        "Bovine_TB": "A chronic bacterial infection that can spread via air or raw milk.",
        "Anthrax": "A serious infection caused by spores, linked to carcasses and contaminated soil.",
        "Q_Fever": "A bacterial infection often linked to inhaling dust from birth fluids.",
        "FMD": "A viral livestock disease; human infection is rare but possible with exposure.",
        "LSD": "A viral cattle disease; not considered directly transmissible to humans.",
        "Ringworm": "A fungal skin infection that spreads through direct contact and surfaces.",
    }.get(disease, "Zoonotic disease screening result.")


def _zoonotic_classification(disease: str) -> str:
    if disease == "LSD":
        return "Low zoonotic concern (not directly transmissible to humans)"
    return "Zoonotic concern present (clinical confirmation needed)"


def _generate_reference() -> str:
    return f"LG-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"


@router.post("/symptom-report")
def generate_symptom_report(payload: SymptomReportRequest) -> dict:
    ref = _generate_reference()
    filename = f"symptom_{ref}.pdf"
    out_path = REPORTS_DIR / filename

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
        from reportlab.lib.units import cm
    except Exception:
        raise HTTPException(status_code=500, detail="ReportLab not installed on server")

    doc = SimpleDocTemplate(str(out_path), pagesize=A4, title="LivestockGuard — Doctor Visit Report")
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>LivestockGuard — Doctor Visit Report</b>", styles["Title"]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(f"<b>Reference:</b> {ref}", styles["Normal"]))
    story.append(Paragraph(f"<b>Date:</b> {datetime.now().date().isoformat()}", styles["Normal"]))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("<b>Section 1 — Suspected Disease</b>", styles["Heading2"]))
    story.append(Paragraph(f"<b>Disease:</b> {payload.disease}", styles["Normal"]))
    story.append(Paragraph(f"<b>Description:</b> {_disease_description(payload.disease)}", styles["Normal"]))
    story.append(Paragraph(f"<b>Zoonotic classification:</b> {_zoonotic_classification(payload.disease)}", styles["Normal"]))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("<b>Section 2 — Patient Exposure History</b>", styles["Heading2"]))
    exposures_true = [k.replace("_", " ").title() for k, v in payload.exposure_summary.items() if v]
    if exposures_true:
        story.append(Paragraph("• " + "<br/>• ".join(exposures_true), styles["Normal"]))
    else:
        story.append(Paragraph("No exposures reported.", styles["Normal"]))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("<b>Section 3 — Symptoms the Patient is Reporting</b>", styles["Heading2"]))
    if payload.symptoms_reported:
        story.append(Paragraph("• " + "<br/>• ".join(payload.symptoms_reported), styles["Normal"]))
    else:
        story.append(Paragraph("No symptoms reported.", styles["Normal"]))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("<b>Section 4 — Risk Assessment</b>", styles["Heading2"]))
    story.append(Paragraph(f"<b>Risk score:</b> {payload.risk_score}", styles["Normal"]))
    story.append(Paragraph(f"<b>Risk tier:</b> {payload.risk_tier}", styles["Normal"]))
    groups = HOUSEHOLD_RISK_GROUPS.get(payload.disease, [])
    story.append(Paragraph(f"<b>At-risk household groups:</b> {', '.join(groups) if groups else 'None flagged'}", styles["Normal"]))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("<b>Section 5 — Recommended Tests</b>", styles["Heading2"]))
    tests = _recommended_tests(payload.disease)
    story.append(Paragraph("• " + "<br/>• ".join(tests), styles["Normal"]))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("<b>Section 6 — Note to Doctor</b>", styles["Heading2"]))
    story.append(
        Paragraph(
            "This report was generated by LivestockGuard, a zoonotic disease screening tool. "
            "This is not a diagnosis. Please use clinical judgment.",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(f"<i>LivestockGuard reference number: {ref}</i>", styles["Normal"]))

    doc.build(story)

    return {"pdf_url": f"/reports/{filename}", "reference_number": ref}

