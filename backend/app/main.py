from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from app.db.init_db import init_database, seed_from_matrix_if_needed
from app.db.session import SessionLocal
from app.routes import (
    auth_router,
    calendar_router,
    catalog_router,
    cluster_router,
    detection_router,
    device_router,
    report_router,
    risk_router,
)
from app.services.model_service import load_models_once

BASE_PATH = Path(__file__).resolve().parents[1]


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_database()
    load_models_once(BASE_PATH)
    with SessionLocal() as db:
        seed_from_matrix_if_needed(BASE_PATH, db)
    yield


app = FastAPI(title="LivestockGuard API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detection_router)
app.include_router(catalog_router)
app.include_router(calendar_router)
app.include_router(report_router)
app.include_router(risk_router)
app.include_router(auth_router)
app.include_router(cluster_router)
app.include_router(device_router)

# Serve generated PDFs
app.mount("/reports", StaticFiles(directory=str(BASE_PATH / "reports")), name="reports")


@app.get("/", response_class=PlainTextResponse)
def home() -> str:
    return "LivestockGuard backend running"

