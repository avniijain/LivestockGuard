from __future__ import annotations

from pathlib import Path

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine
from app.models import ClusterAlert, ClusterAlertNotification, DeviceToken, Disease, DiseaseSymptom, Report, Symptom, TransmissionRoute, User, UserLocation  # noqa: F401

VISUAL_DISEASES = {"lsd", "fmd", "ringworm", "healthy"}
DEFAULT_ROUTES = ("contact", "milk", "air", "urine")


def init_database() -> None:
    Base.metadata.create_all(bind=engine)


def seed_from_matrix_if_needed(base_path: Path, db: Session) -> None:
    existing = db.scalar(select(Disease.id).limit(1))
    if existing:
        return

    matrix_path = base_path / "symptom_disease_matrix.csv"
    if not matrix_path.exists():
        return

    matrix = pd.read_csv(matrix_path)
    symptom_columns = [c for c in matrix.columns if c != "Disease"]

    symptoms_map: dict[str, Symptom] = {}
    for name in symptom_columns:
        symptom = Symptom(name=name)
        db.add(symptom)
        symptoms_map[name] = symptom
    db.flush()

    for _, row in matrix.iterrows():
        disease_name = str(row["Disease"]).strip()
        disease_type = "visual" if disease_name.lower() in VISUAL_DISEASES else "symptom"
        disease = Disease(name=disease_name, type=disease_type, zoonotic=(disease_name.lower() != "healthy"))
        db.add(disease)
        db.flush()

        for symptom_name in symptom_columns:
            db.add(
                DiseaseSymptom(
                    disease_id=disease.id,
                    symptom_id=symptoms_map[symptom_name].id,
                    probability=float(row[symptom_name]),
                )
            )

        top_prob = max(float(row[s]) for s in symptom_columns)
        for route in DEFAULT_ROUTES:
            db.add(
                TransmissionRoute(
                    disease_id=disease.id,
                    route=route,
                    base_probability=round(max(0.01, top_prob * (0.6 if route == "contact" else 0.35)), 3),
                )
            )

    db.commit()
