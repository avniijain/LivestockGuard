from pydantic import BaseModel, Field


class HeatmapPoint(BaseModel):
    id: int
    disease: str
    latitude: float
    longitude: float
    confidence: float
    timestamp: str


class ClusterOut(BaseModel):
    disease: str
    severity: str
    case_count: int
    centroid_lat: float
    centroid_lng: float
    distance_km: float | None = None


class NearbyClustersResponse(BaseModel):
    clusters: list[ClusterOut]
    heatmap_points: list[HeatmapPoint]
    window_days: int = 7
    cluster_rule: str = "3+ cases, same disease, within 10 km, within 7 days"
