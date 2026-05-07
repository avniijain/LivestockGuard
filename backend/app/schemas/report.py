from datetime import datetime

from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    disease_predicted: str
    confidence: float = Field(ge=0, le=1)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class ReportOut(BaseModel):
    id: int
    disease_predicted: str
    confidence: float
    latitude: float
    longitude: float
    timestamp: datetime

    model_config = {"from_attributes": True}

