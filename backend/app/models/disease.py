from __future__ import annotations

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Disease(Base):
    __tablename__ = "diseases"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(20), nullable=False)  # visual | symptom
    zoonotic: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    symptoms = relationship("DiseaseSymptom", back_populates="disease", cascade="all, delete-orphan")
    transmission_routes = relationship(
        "TransmissionRoute",
        back_populates="disease",
        cascade="all, delete-orphan",
    )

