from __future__ import annotations

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TransmissionRoute(Base):
    __tablename__ = "transmission_routes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    disease_id: Mapped[int] = mapped_column(ForeignKey("diseases.id", ondelete="CASCADE"), nullable=False, index=True)
    route: Mapped[str] = mapped_column(String(60), nullable=False)
    base_probability: Mapped[float] = mapped_column(Float, nullable=False, default=0.1)

    disease = relationship("Disease", back_populates="transmission_routes")

