from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ClusterAlertNotification(Base):
    __tablename__ = "cluster_alert_notifications"
    __table_args__ = (UniqueConstraint("alert_id", "device_token_id", name="uq_alert_device_token"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    alert_id: Mapped[int] = mapped_column(ForeignKey("cluster_alerts.id"), nullable=False, index=True)
    device_token_id: Mapped[int] = mapped_column(ForeignKey("device_tokens.id"), nullable=False, index=True)
    sent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
