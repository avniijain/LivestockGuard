from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.session import engine  # noqa: E402
from app.models import (  # noqa: E402
    ClusterAlert,
    ClusterAlertNotification,
    DeviceToken,
    Disease,
    DiseaseSymptom,
    Report,
    Symptom,
    TransmissionRoute,
    User,
    UserLocation,
)

TABLES = [
    Disease,
    Symptom,
    DiseaseSymptom,
    User,
    Report,
    ClusterAlert,
    DeviceToken,
    UserLocation,
    TransmissionRoute,
    ClusterAlertNotification,
]

JSON_COLUMNS = {
    "reports": {"exposure_summary", "symptoms_reported"},
}


def _table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def _decode_json(value: Any) -> Any:
    if value in (None, "") or not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def _rows_for_table(conn: sqlite3.Connection, table_name: str) -> list[dict[str, Any]]:
    if not _table_exists(conn, table_name):
        return []
    conn.row_factory = sqlite3.Row
    rows = []
    json_columns = JSON_COLUMNS.get(table_name, set())
    for row in conn.execute(f'SELECT * FROM "{table_name}"'):
        item = dict(row)
        for column in json_columns:
            if column in item:
                item[column] = _decode_json(item[column])
        rows.append(item)
    return rows


def _truncate_postgres_tables() -> None:
    table_names = ", ".join(f'"{model.__tablename__}"' for model in reversed(TABLES))
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {table_names} RESTART IDENTITY CASCADE"))


def _reset_sequences() -> None:
    with engine.begin() as conn:
        for model in TABLES:
            table = model.__table__
            if "id" not in table.c:
                continue
            conn.execute(
                text(
                    """
                    SELECT setval(
                        pg_get_serial_sequence(:table_name, 'id'),
                        COALESCE((SELECT MAX(id) FROM {table_name}), 1),
                        (SELECT COUNT(*) > 0 FROM {table_name})
                    )
                    """.format(table_name=f'"{model.__tablename__}"')
                ),
                {"table_name": model.__tablename__},
            )


def migrate(sqlite_path: Path, *, truncate: bool) -> None:
    if not sqlite_path.exists():
        raise FileNotFoundError(f"SQLite database not found: {sqlite_path}")

    if truncate:
        _truncate_postgres_tables()

    with sqlite3.connect(sqlite_path) as sqlite_conn, engine.begin() as postgres_conn:
        for model in TABLES:
            table = model.__table__
            rows = _rows_for_table(sqlite_conn, model.__tablename__)
            if not rows:
                continue
            allowed = set(table.c.keys())
            clean_rows = [{key: value for key, value in row.items() if key in allowed} for row in rows]
            stmt = insert(table).values(clean_rows).on_conflict_do_nothing()
            postgres_conn.execute(stmt)

    _reset_sequences()


def main() -> None:
    parser = argparse.ArgumentParser(description="Copy LivestockGuard data from SQLite into PostgreSQL.")
    parser.add_argument(
        "--sqlite-path",
        type=Path,
        default=BACKEND_ROOT / "livestockguard.db",
        help="Path to the existing SQLite database file.",
    )
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="Clear PostgreSQL LivestockGuard tables before importing.",
    )
    args = parser.parse_args()

    migrate(args.sqlite_path, truncate=args.truncate)
    print("SQLite data migration to PostgreSQL completed.")


if __name__ == "__main__":
    main()
