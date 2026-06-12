from __future__ import annotations

import logging
import os
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cluster_alert import ClusterAlert
from app.models.cluster_alert_notification import ClusterAlertNotification
from app.models.device_token import DeviceToken
from app.models.user_location import UserLocation
from app.services.cluster_service import CLUSTER_EPS_KM, haversine_km

logger = logging.getLogger(__name__)

_firebase_app = None


def _disease_display(name: str) -> str:
    key = name.strip().lower().replace(" ", "_")
    labels = {
        "fmd": "Foot and Mouth Disease",
        "lsd": "Lumpy Skin Disease",
        "brucellosis": "Brucellosis",
        "leptospirosis": "Leptospirosis",
        "ringworm": "Ringworm",
        "anthrax": "Anthrax",
        "bovine_tb": "Bovine Tuberculosis",
        "q_fever": "Q Fever",
    }
    return labels.get(key, name.replace("_", " ").title())


def _init_firebase():
    global _firebase_app
    if _firebase_app is not None:
        return _firebase_app

    try:
        import firebase_admin
        from firebase_admin import credentials
    except ImportError:
        logger.warning("firebase-admin not installed; push notifications disabled.")
        return None

    if firebase_admin._apps:
        _firebase_app = firebase_admin.get_app()
        return _firebase_app

    cred_path = os.getenv(
        "FIREBASE_CREDENTIALS_PATH",
        str(Path(__file__).resolve().parents[2] / "firebase" / "serviceAccountKey.json"),
    )
    if not Path(cred_path).exists():
        logger.warning("Firebase credentials not found at %s; push notifications disabled.", cred_path)
        return None

    cred = credentials.Certificate(cred_path)
    _firebase_app = firebase_admin.initialize_app(cred)
    return _firebase_app


def notify_cluster_alert(db: Session, alert: ClusterAlert) -> int:
    """Send FCM to devices within cluster alert radius. Returns count sent."""
    if _init_firebase() is None:
        return 0

    from firebase_admin import messaging

    locations = list(db.scalars(select(UserLocation)).all())
    if not locations:
        logger.info("No user locations stored; skipping FCM for alert id=%s", alert.id)
        return 0

    radius_km = CLUSTER_EPS_KM
    sent = 0

    for loc in locations:
        distance = haversine_km(loc.latitude, loc.longitude, alert.centroid_lat, alert.centroid_lng)
        if distance > radius_km:
            continue

        device = db.scalar(select(DeviceToken).where(DeviceToken.token == loc.device_token))
        if device is None:
            continue

        existing = db.scalar(
            select(ClusterAlertNotification).where(
                ClusterAlertNotification.alert_id == alert.id,
                ClusterAlertNotification.device_token_id == device.id,
            )
        )
        if existing is not None:
            continue

        disease_label = _disease_display(alert.disease)
        body = (
            f"High-risk {disease_label} cluster detected within "
            f"{int(radius_km)} km of your location."
        )

        try:
            messaging.send(
                messaging.Message(
                    notification=messaging.Notification(
                        title="Disease Outbreak Alert",
                        body=body,
                    ),
                    data={
                        "type": "cluster_alert",
                        "alert_id": str(alert.id),
                        "disease": alert.disease,
                        "severity": alert.severity,
                    },
                    token=device.token,
                )
            )
            db.add(ClusterAlertNotification(alert_id=alert.id, device_token_id=device.id))
            db.commit()
            sent += 1
        except Exception:
            logger.exception("Failed to send FCM to token id=%s", device.id)
            db.rollback()

    if sent:
        logger.info("Sent %s FCM outbreak alert(s) for alert id=%s", sent, alert.id)
    return sent
