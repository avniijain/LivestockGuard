from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.disease import Disease
from app.models.report import Report
from app.models.transmission_route import TransmissionRoute
from app.schemas.risk import ExposureInput

ANIMAL_GUIDANCE: dict[str, dict[str, str]] = {
    "Brucellosis": {
        "immediate": "Isolate the animal from the rest of the herd immediately.",
        "do_not": "Do not allow the animal to breed. Do not consume its milk until tested.",
        "vet_action": "Request a Rose Bengal Plate Test (RBPT) from a government vet.",
        "recovery": "Brucellosis has no cure in cattle. If confirmed, the animal may need to be culled per government protocol.",
    },
    "Leptospirosis": {
        "immediate": "Keep the animal away from water sources and other cattle.",
        "do_not": "Do not let the animal wade in common water troughs or ponds.",
        "vet_action": "A government vet can prescribe antibiotics (penicillin/streptomycin) — effective if caught early.",
        "recovery": "Most cattle recover with antibiotic treatment within 1–2 weeks.",
    },
    "Bovine_TB": {
        "immediate": "Isolate the animal. Avoid close contact — especially in enclosed spaces.",
        "do_not": "Do not sell or transport the animal. Do not consume raw milk.",
        "vet_action": "Request a Tuberculin Skin Test (TST) from a government vet. Notify your district animal husbandry officer — bTB is notifiable.",
        "recovery": "There is no approved treatment for bTB in cattle in India. Confirmed cases are typically culled under the National TB programme.",
    },
    "Anthrax": {
        "immediate": "Do NOT move, open, or skin the carcass if the animal has died. Anthrax spores spread when a carcass is disturbed.",
        "do_not": "Do not allow any person or other animal near the carcass. Do not consume any part of the animal.",
        "vet_action": "Call the district veterinary officer immediately — Anthrax is a notifiable disease. Surviving animals can be vaccinated.",
        "recovery": "Anthrax in cattle is often fatal. If alive, high-dose penicillin may be administered by a vet.",
    },
    "Q_Fever": {
        "immediate": "Isolate the animal, especially during and after birthing.",
        "do_not": "Do not handle birth fluids, placenta, or aborted material without heavy gloves and a mask.",
        "vet_action": "A vet can prescribe tetracycline. Vaccination is available in some states.",
        "recovery": "Most cattle recover, but they can remain carriers and shed Coxiella in milk and birth fluids.",
    },
    "LSD": {
        "immediate": "Isolate the animal to prevent insect vector spread to other cattle.",
        "do_not": "Do not move the animal off your farm. Do not allow insect exposure.",
        "vet_action": "Contact a vet for supportive care (wound treatment, fly repellent). Vaccination campaign may be available in your district.",
        "recovery": "Most cattle recover in 2–6 weeks with proper wound care and fly control.",
    },
    "FMD": {
        "immediate": "Isolate the animal. Restrict all movement on and off your farm immediately.",
        "do_not": "Do not sell or move any cattle. FMD spreads extremely rapidly between herds.",
        "vet_action": "FMD is notifiable — call your district vet officer. Vaccination of surrounding herd is the primary control measure.",
        "recovery": "Most cattle survive FMD but recovery can take 2–3 weeks. Milk production may drop permanently.",
    },
    "Ringworm": {
        "immediate": "Separate the affected animal. Wear gloves when handling.",
        "do_not": "Do not let children touch the animal. Do not share grooming equipment between animals.",
        "vet_action": "A vet can prescribe antifungal spray or iodine-based wash. Treat all contact animals.",
        "recovery": "Ringworm typically resolves in 1–3 months with treatment. It is not life-threatening.",
    },
}


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
        "animal_guidance": ANIMAL_GUIDANCE.get(disease.name, {}),
    }

