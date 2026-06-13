from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker
from dotenv import load_dotenv

BACKEND_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_ROOT / ".env")


def _postgres_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is required and must point to PostgreSQL, for example "
            "postgresql+psycopg://postgres:postgres@localhost:5432/livestockguard"
        )

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    url = make_url(database_url)
    if not url.drivername.startswith("postgresql"):
        raise RuntimeError("DATABASE_URL must use a PostgreSQL SQLAlchemy driver, preferably postgresql+psycopg.")
    if url.drivername == "postgresql":
        raise RuntimeError("DATABASE_URL must include a PostgreSQL driver, preferably postgresql+psycopg.")
    return database_url


DATABASE_URL = _postgres_database_url()

engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 10},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

