from datetime import datetime

from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    disease_predicted: str
    confidence: float = Field(ge=0, le=1)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    risk_score: int | None = Field(default=None, ge=0, le=100)
    risk_tier: str | None = None
    source: str = Field(default="image", max_length=30)
    device_token: str | None = Field(default=None, max_length=512)
    exposure_summary: dict[str, bool] | None = None
    symptoms_reported: list[str] | None = None


class ReportOut(BaseModel):
    id: int
    disease_predicted: str
    confidence: float
    latitude: float
    longitude: float
    risk_score: int | None = None
    risk_tier: str | None = None
    source: str
    exposure_summary: dict[str, bool] | None = None
    symptoms_reported: list[str] | None = None
    pdf_reference: str | None = None
    pdf_url: str | None = None
    timestamp: datetime
    cluster_alert: str | None = None

    model_config = {"from_attributes": True}


class ReportHistoryOut(BaseModel):
    reports: list[ReportOut]
    total: int
