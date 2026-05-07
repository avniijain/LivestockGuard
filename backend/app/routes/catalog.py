from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.disease import Disease
from app.models.symptom import Symptom
from app.schemas.disease import DiseaseOut
from app.schemas.symptom import SymptomOut

router = APIRouter(tags=["Catalog"])


@router.get("/diseases", response_model=list[DiseaseOut])
def list_diseases(db: Session = Depends(get_db)) -> list[Disease]:
    return list(db.scalars(select(Disease).order_by(Disease.name)).all())


@router.get("/symptoms", response_model=list[SymptomOut])
def list_symptoms(db: Session = Depends(get_db)) -> list[Symptom]:
    return list(db.scalars(select(Symptom).order_by(Symptom.name)).all())

