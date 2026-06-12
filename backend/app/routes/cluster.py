from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.cluster import ClusterOut, HeatmapPoint, NearbyClustersResponse
from app.services.cluster_service import clusters_near, haversine_km

router = APIRouter(prefix="/clusters", tags=["Clusters"])


@router.get("/nearby", response_model=NearbyClustersResponse)
def nearby_clusters(
    lat: float = Query(ge=-90, le=90),
    lng: float = Query(ge=-180, le=180),
    radius_km: float = Query(default=25.0, ge=1, le=100),
    disease: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> dict:
    nearby, points = clusters_near(db, lat, lng, radius_km=radius_km, disease=disease)

    return {
        "clusters": [
            ClusterOut(
                disease=c.disease,
                severity=c.severity,
                case_count=c.case_count,
                centroid_lat=c.centroid_lat,
                centroid_lng=c.centroid_lng,
                distance_km=round(haversine_km(lat, lng, c.centroid_lat, c.centroid_lng), 2),
            )
            for c in nearby
        ],
        "heatmap_points": [
            HeatmapPoint(
                id=p.id,
                disease=p.disease_predicted,
                latitude=p.latitude,
                longitude=p.longitude,
                confidence=p.confidence,
                timestamp=p.timestamp.isoformat(),
            )
            for p in points
        ],
    }
