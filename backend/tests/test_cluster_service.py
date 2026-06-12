"""Tests for DBSCAN cluster detection and outbreak notification rules."""

from datetime import datetime, timezone

from app.models.cluster_alert import ClusterAlert
from app.models.report import Report
from app.services.cluster_service import (
    CLUSTER_MIN_SAMPLES,
    ClusterSummary,
    detect_clusters,
    should_notify_for_cluster,
)


def _report(disease: str, lat: float, lng: float, rid: int) -> Report:
    return Report(
        id=rid,
        disease_predicted=disease,
        confidence=0.8,
        latitude=lat,
        longitude=lng,
        timestamp=datetime.now(timezone.utc),
    )


def test_detect_cluster_three_nearby_fmd_cases():
    reports = [
        _report("fmd", 28.6139, 77.2090, 1),
        _report("fmd", 28.6150, 77.2100, 2),
        _report("fmd", 28.6145, 77.2085, 3),
    ]
    clusters = detect_clusters(reports)
    assert len(clusters) == 1
    assert clusters[0].disease == "fmd"
    assert clusters[0].case_count >= CLUSTER_MIN_SAMPLES


def test_isolated_reports_no_cluster():
    reports = [
        _report("fmd", 28.61, 77.20, 1),
        _report("fmd", 29.50, 78.00, 2),
    ]
    assert detect_clusters(reports) == []


def test_multiple_fmd_clusters_in_different_locations():
    near_delhi = [
        _report("fmd", 28.6139, 77.2090, 1),
        _report("fmd", 28.6150, 77.2100, 2),
        _report("fmd", 28.6145, 77.2085, 3),
    ]
    near_mumbai = [
        _report("fmd", 19.0760, 72.8777, 4),
        _report("fmd", 19.0770, 72.8785, 5),
        _report("fmd", 19.0765, 72.8770, 6),
    ]
    clusters = detect_clusters(near_delhi + near_mumbai)
    assert len(clusters) == 2
    assert all(c.disease == "fmd" for c in clusters)


def _cluster(case_count: int, severity: str, lat: float, lng: float) -> ClusterSummary:
    return ClusterSummary(
        disease="fmd",
        severity=severity,
        case_count=case_count,
        centroid_lat=lat,
        centroid_lng=lng,
        report_ids=list(range(1, case_count + 1)),
    )


def _prior_alert(severity: str, case_count: int, lat: float, lng: float) -> ClusterAlert:
    return ClusterAlert(
        id=1,
        disease="fmd",
        severity=severity,
        centroid_lat=lat,
        centroid_lng=lng,
        case_count=case_count,
    )


def test_notify_on_new_cluster():
    cluster = _cluster(3, "moderate", 28.614, 77.209)
    assert should_notify_for_cluster(cluster, None) is True


def test_no_notify_when_case_count_grows_same_severity():
    cluster = _cluster(4, "moderate", 28.6145, 77.2095)
    prior = _prior_alert("moderate", 3, 28.614, 77.209)
    assert should_notify_for_cluster(cluster, prior) is False


def test_notify_on_severity_escalation():
    cluster = _cluster(5, "high", 28.6145, 77.2095)
    prior = _prior_alert("moderate", 4, 28.614, 77.209)
    assert should_notify_for_cluster(cluster, prior) is True


def test_notify_on_cluster_geographic_expansion():
    cluster = _cluster(4, "moderate", 28.700, 77.300)
    prior = _prior_alert("moderate", 3, 28.614, 77.209)
    assert should_notify_for_cluster(cluster, prior) is True
