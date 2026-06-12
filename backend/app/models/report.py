from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    disease_predicted: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    risk_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    risk_tier: Mapped[str | None] = mapped_column(String(20), nullable=True)
    source: Mapped[str] = mapped_column(String(30), nullable=False, default="image")
    exposure_summary: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    symptoms_reported: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    pdf_reference: Mapped[str | None] = mapped_column(String(40), nullable=True)
    pdf_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
