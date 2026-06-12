from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.ml.bayesian_risk import compute_risk_score
from app.ml.watch_calendar import _canonical_disease
from app.schemas.risk import BayesianRiskOut, BayesianRiskRequest, ExposureInput, HumanRiskOut
from app.services.risk_service import calculate_human_risk

router = APIRouter(prefix="/risk", tags=["Risk"])


@router.post("/human", response_model=BayesianRiskOut | HumanRiskOut)
def compute_human_risk(
    payload: BayesianRiskRequest | ExposureInput,
    db: Session = Depends(get_db),
) -> dict:
    """
    Backwards compatible endpoint:
    - New format: { disease, exposure{...} } -> Bayesian risk output
    - Old format: ExposureInput (uses last report disease) -> legacy output
    """
    try:
        if isinstance(payload, BayesianRiskRequest):
            exposure = payload.exposure.model_dump()
            disease = _canonical_disease(payload.disease)
            return compute_risk_score(disease, exposure)
        return calculate_human_risk(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to compute risk")

