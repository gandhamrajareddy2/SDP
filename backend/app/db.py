import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from .config import DB_PATH


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = _connect()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS datasets (
                dataset_id TEXT PRIMARY KEY,
                dataset_name TEXT NOT NULL,
                csv_path TEXT NOT NULL,
                rows_count INTEGER NOT NULL,
                columns_count INTEGER NOT NULL,
                difficulty TEXT NOT NULL,
                include_missing_values INTEGER NOT NULL,
                include_outliers INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def save_dataset_record(
    dataset_id: str,
    dataset_name: str,
    csv_path: Path,
    rows_count: int,
    columns_count: int,
    difficulty: str,
    include_missing_values: bool,
    include_outliers: bool,
) -> None:
    conn = _connect()
    try:
        conn.execute(
            """
            INSERT INTO datasets (
                dataset_id,
                dataset_name,
                csv_path,
                rows_count,
                columns_count,
                difficulty,
                include_missing_values,
                include_outliers,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                dataset_id,
                dataset_name,
                str(csv_path),
                rows_count,
                columns_count,
                difficulty,
                int(include_missing_values),
                int(include_outliers),
                datetime.now(tz=timezone.utc).isoformat(),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def get_dataset_record(dataset_id: str) -> sqlite3.Row | None:
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT * FROM datasets WHERE dataset_id = ?", (dataset_id,)
        ).fetchone()
        return row
    finally:
        conn.close()


def delete_dataset_record(dataset_id: str) -> None:
    conn = _connect()
    try:
        conn.execute("DELETE FROM datasets WHERE dataset_id = ?", (dataset_id,))
        conn.commit()
    finally:
        conn.close()


def list_dataset_records(limit: int = 20) -> list[sqlite3.Row]:
    conn = _connect()
    try:
        rows = conn.execute(
            """
            SELECT *
            FROM datasets
            ORDER BY datetime(created_at) DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return rows
    finally:
        conn.close()
