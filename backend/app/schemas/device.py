from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class DeviceTokenCreate(BaseModel):
    token: str = Field(min_length=10, max_length=512)


class DeviceTokenOut(BaseModel):
    id: int
    user_id: int | None
    token: str
    last_seen: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class UserLocationUpdate(BaseModel):
    device_token: str = Field(min_length=10, max_length=512)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class UserLocationOut(BaseModel):
    id: int
    user_id: int | None
    device_token: str
    latitude: float
    longitude: float
    updated_at: datetime

    model_config = {"from_attributes": True}
