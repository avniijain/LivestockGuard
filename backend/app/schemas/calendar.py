from pydantic import BaseModel, Field


class CalendarOut(BaseModel):
    disease: str
    exposure_date: str
    watch_start: str
    watch_end: str
    danger_window_start: str
    danger_window_end: str
    symptoms: list[str]
    total_watch_days: int


class SymptomReportRequest(BaseModel):
    disease: str
    exposure_date: str
    risk_score: int = Field(ge=0, le=100)
    risk_tier: str
    symptoms_reported: list[str]
    exposure_summary: dict[str, bool]

