from app.routes.catalog import router as catalog_router
from app.routes.calendar import router as calendar_router
from app.routes.detection import router as detection_router
from app.routes.report import router as report_router
from app.routes.risk import router as risk_router

__all__ = ["detection_router", "catalog_router", "calendar_router", "report_router", "risk_router"]

