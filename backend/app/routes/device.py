from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps.auth import get_current_user_optional
from app.models.device_token import DeviceToken
from app.models.user import User
from app.models.user_location import UserLocation
from app.schemas.device import DeviceTokenCreate, DeviceTokenOut, UserLocationOut, UserLocationUpdate
from app.services.device_service import register_device_token, upsert_user_location

router = APIRouter(tags=["Device"])


@router.post("/device-token", response_model=DeviceTokenOut)
def upsert_device_token(
    payload: DeviceTokenCreate,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
) -> DeviceToken:
    return register_device_token(db, payload.token.strip(), user)


@router.post("/user-location", response_model=UserLocationOut)
def update_user_location(
    payload: UserLocationUpdate,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
) -> UserLocation:
    return upsert_user_location(
        db,
        device_token=payload.device_token.strip(),
        latitude=payload.latitude,
        longitude=payload.longitude,
        user=user,
    )
