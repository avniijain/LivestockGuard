from __future__ import annotations

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class DiseaseSymptom(Base):
    __tablename__ = "disease_symptoms"

    disease_id: Mapped[int] = mapped_column(ForeignKey("diseases.id", ondelete="CASCADE"), primary_key=True)
    symptom_id: Mapped[int] = mapped_column(ForeignKey("symptoms.id", ondelete="CASCADE"), primary_key=True)
    probability: Mapped[float] = mapped_column(Float, nullable=False)

    disease = relationship("Disease", back_populates="symptoms")
    symptom = relationship("Symptom", back_populates="diseases")

