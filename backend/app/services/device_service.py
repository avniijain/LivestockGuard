from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.device_token import DeviceToken
from app.models.user import User
from app.models.user_location import UserLocation


def register_device_token(db: Session, token: str, user: User | None) -> DeviceToken:
    row = db.scalar(select(DeviceToken).where(DeviceToken.token == token))
    now = datetime.now(timezone.utc)
    if row is None:
        row = DeviceToken(token=token, user_id=user.id if user else None, last_seen=now)
        db.add(row)
    else:
        row.last_seen = now
        if user is not None:
            row.user_id = user.id
    db.commit()
    db.refresh(row)
    return row


def upsert_user_location(
    db: Session,
    *,
    device_token: str,
    latitude: float,
    longitude: float,
    user: User | None,
) -> UserLocation:
    row = db.scalar(select(UserLocation).where(UserLocation.device_token == device_token))
    if row is None:
        row = UserLocation(
            device_token=device_token,
            user_id=user.id if user else None,
            latitude=latitude,
            longitude=longitude,
        )
        db.add(row)
    else:
        row.latitude = latitude
        row.longitude = longitude
        row.updated_at = datetime.now(timezone.utc)
        if user is not None:
            row.user_id = user.id
    db.commit()
    db.refresh(row)
    return row
