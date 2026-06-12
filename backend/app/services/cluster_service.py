from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import numpy as np
from sklearn.cluster import DBSCAN
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cluster_alert import ClusterAlert
from app.models.report import Report

EARTH_RADIUS_KM = 6371.0
CLUSTER_EPS_KM = 10.0
CLUSTER_MIN_SAMPLES = 3
CLUSTER_WINDOW_DAYS = 7
CLUSTER_MATCH_KM = CLUSTER_EPS_KM
CLUSTER_EXPANSION_KM = 5.0

_SEVERITY_RANK = {"moderate": 1, "high": 2, "critical": 3}


@dataclass
class ClusterSummary:
    disease: str
    severity: str
    case_count: int
    centroid_lat: float
    centroid_lng: float
    report_ids: list[int]


def _norm_disease(name: str) -> str:
    return str(name).strip().lower().replace(" ", "_")


def _severity(case_count: int) -> str:
    if case_count >= 10:
        return "critical"
    if case_count >= 5:
        return "high"
    return "moderate"


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _recent_reports(db: Session, *, disease: str | None = None) -> list[Report]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=CLUSTER_WINDOW_DAYS)
    rows = list(db.scalars(select(Report).where(Report.timestamp >= cutoff)).all())
    if disease:
        key = _norm_disease(disease)
        return [r for r in rows if _norm_disease(r.disease_predicted) == key]
    return rows


def detect_clusters(reports: list[Report]) -> list[ClusterSummary]:
    if len(reports) < CLUSTER_MIN_SAMPLES:
        return []

    by_disease: dict[str, list[Report]] = {}
    for report in reports:
        key = _norm_disease(report.disease_predicted)
        if key in {"healthy", "uncertain", "not_cow"}:
            continue
        by_disease.setdefault(key, []).append(report)

    clusters: list[ClusterSummary] = []
    eps_rad = CLUSTER_EPS_KM / EARTH_RADIUS_KM

    for disease, group in by_disease.items():
        if len(group) < CLUSTER_MIN_SAMPLES:
            continue

        coords = np.radians([[r.latitude, r.longitude] for r in group])
        labels = DBSCAN(eps=eps_rad, min_samples=CLUSTER_MIN_SAMPLES, metric="haversine").fit_predict(coords)

        label_to_reports: dict[int, list[Report]] = {}
        for label, report in zip(labels, group):
            if label == -1:
                continue
            label_to_reports.setdefault(int(label), []).append(report)

        for members in label_to_reports.values():
            count = len(members)
            if count < CLUSTER_MIN_SAMPLES:
                continue
            lat = sum(m.latitude for m in members) / count
            lng = sum(m.longitude for m in members) / count
            clusters.append(
                ClusterSummary(
                    disease=disease,
                    severity=_severity(count),
                    case_count=count,
                    centroid_lat=lat,
                    centroid_lng=lng,
                    report_ids=[m.id for m in members],
                )
            )

    return clusters


def clusters_near(
    db: Session,
    lat: float,
    lng: float,
    radius_km: float = 25.0,
    disease: str | None = None,
) -> tuple[list[ClusterSummary], list[Report]]:
    reports = _recent_reports(db, disease=disease)
    all_clusters = detect_clusters(reports)
    nearby_clusters = [
        c
        for c in all_clusters
        if haversine_km(lat, lng, c.centroid_lat, c.centroid_lng) <= radius_km
    ]

    heatmap_points = [
        r
        for r in reports
        if haversine_km(lat, lng, r.latitude, r.longitude) <= radius_km
    ]
    return nearby_clusters, heatmap_points


def _find_matching_cluster_alert(db: Session, cluster: ClusterSummary) -> ClusterAlert | None:
    """Most recent alert for the same disease within the cluster match radius."""
    prior_alerts = db.scalars(
        select(ClusterAlert)
        .where(ClusterAlert.disease == cluster.disease)
        .order_by(ClusterAlert.created_at.desc())
    ).all()
    for alert in prior_alerts:
        if (
            haversine_km(alert.centroid_lat, alert.centroid_lng, cluster.centroid_lat, cluster.centroid_lng)
            <= CLUSTER_MATCH_KM
        ):
            return alert
    return None


def should_notify_for_cluster(cluster: ClusterSummary, prior: ClusterAlert | None) -> bool:
    """
    Notify only when:
    - a new geographic cluster is first detected,
    - severity escalates (moderate -> high -> critical), or
    - the cluster centroid shifts beyond CLUSTER_EXPANSION_KM (geographic spread).
    """
    if prior is None:
        return True

    prior_rank = _SEVERITY_RANK.get(prior.severity, 0)
    new_rank = _SEVERITY_RANK.get(cluster.severity, 0)
    if new_rank > prior_rank:
        return True

    centroid_shift_km = haversine_km(
        prior.centroid_lat, prior.centroid_lng, cluster.centroid_lat, cluster.centroid_lng
    )
    if centroid_shift_km >= CLUSTER_EXPANSION_KM:
        return True

    return False


def maybe_record_cluster_alert(db: Session, cluster: ClusterSummary) -> ClusterAlert | None:
    prior = _find_matching_cluster_alert(db, cluster)
    if not should_notify_for_cluster(cluster, prior):
        return None

    alert = ClusterAlert(
        disease=cluster.disease,
        severity=cluster.severity,
        centroid_lat=cluster.centroid_lat,
        centroid_lng=cluster.centroid_lng,
        case_count=cluster.case_count,
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def check_clusters_after_report(
    db: Session, report: Report
) -> tuple[list[ClusterSummary], list[ClusterAlert]]:
    disease_key = _norm_disease(report.disease_predicted)
    reports = _recent_reports(db, disease=disease_key)
    clusters = detect_clusters(reports)
    triggered = [c for c in clusters if report.id in c.report_ids]
    new_alerts: list[ClusterAlert] = []
    for cluster in triggered:
        alert = maybe_record_cluster_alert(db, cluster)
        if alert is not None:
            new_alerts.append(alert)
    return triggered, new_alerts
