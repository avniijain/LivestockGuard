from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import UnidentifiedImageError

from app.schemas.detection import SymptomRequest
from app.services.model_service import predict_image, predict_symptoms

router = APIRouter(prefix="/detect", tags=["Detection"])


@router.post("/image")
async def detect_image(file: UploadFile = File(...)) -> dict:
    # Don't rely on Content-Type for validation: many mobile clients send
    # `application/octet-stream` for multipart file parts even when the bytes are
    # a valid image. We validate using PIL instead.
    try:
        raw = await file.read()
        return predict_image(raw)
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid or unsupported image file")
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to run image prediction")


@router.post("/symptoms")
async def detect_symptoms(payload: SymptomRequest) -> dict:
    try:
        return predict_symptoms(payload)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to run symptom prediction")

