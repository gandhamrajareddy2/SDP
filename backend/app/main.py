from __future__ import annotations

import csv
import math
import statistics
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse

from .config import CORS_ALLOW_CREDENTIALS, CORS_ALLOW_ORIGINS, FRONTEND_DIST_DIR, GENERATED_DIR
from .dataset_generator import (
    generate_dataset as generate_dataset_bundle,
    get_dataset_template,
    get_projects,
)
from .db import delete_dataset_record, get_dataset_record, init_db, list_dataset_records, save_dataset_record
from .schemas import (
    DatasetGenerateRequest,
    DatasetProfileResponse,
    DatasetRecordResponse,
    DatasetSummaryResponse,
    NumericStats,
    PaginatedRowsResponse,
)

app = FastAPI(title="DataScience Lab API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/projects")
def projects() -> list[dict[str, str]]:
    return get_projects()


@app.get("/api/datasets", response_model=list[DatasetRecordResponse])
def list_datasets(limit: int = 20) -> list[DatasetRecordResponse]:
    safe_limit = max(1, min(limit, 100))
    rows = list_dataset_records(limit=safe_limit)
    return [
        DatasetRecordResponse(
            dataset_id=row["dataset_id"],
            dataset_name=row["dataset_name"],
            rows_count=row["rows_count"],
            columns_count=row["columns_count"],
            difficulty=row["difficulty"],
            include_missing_values=bool(row["include_missing_values"]),
            include_outliers=bool(row["include_outliers"]),
            created_at=row["created_at"],
        )
        for row in rows
    ]


def _try_cast(value: str) -> object | None:
    if value == "":
        return None
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        return value


def _infer_dtype(values: list[object | None]) -> str:
    non_null = [value for value in values if value is not None]
    if not non_null:
        return "unknown"
    if all(isinstance(value, int) for value in non_null):
        return "int"
    if all(isinstance(value, (int, float)) for value in non_null):
        return "float"
    return "str"


def _load_rows(csv_path: Path) -> tuple[list[str], list[dict[str, object | None]]]:
    with csv_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise HTTPException(status_code=500, detail="Dataset has no headers")
        rows: list[dict[str, object | None]] = []
        for row in reader:
            parsed: dict[str, object | None] = {}
            for key in reader.fieldnames:
                parsed[key] = _try_cast(row.get(key, ""))
            rows.append(parsed)
        return reader.fieldnames, rows


def _build_summary(
    dataset_id: str,
    dataset_name: str,
    difficulty: str,
    fieldnames: list[str],
    rows: list[dict[str, object | None]],
) -> DatasetSummaryResponse:
    template = get_dataset_template(dataset_name)
    cols_by_name: dict[str, list[object | None]] = {column: [] for column in fieldnames}
    for row in rows:
        for column in fieldnames:
            cols_by_name[column].append(row.get(column))

    return DatasetSummaryResponse(
        dataset_id=dataset_id,
        dataset_name=dataset_name,
        rows=len(rows),
        columns=len(fieldnames),
        target_suggestion=template.target_suggestion,
        difficulty=difficulty,
        column_descriptions=template.column_descriptions,
        data_types={column: _infer_dtype(values) for column, values in cols_by_name.items()},
        missing_summary={
            column: sum(1 for value in values if value is None)
            for column, values in cols_by_name.items()
        },
        preview=rows[:20],
        suggested_questions=template.suggested_questions,
    )


def _search_match(row: dict[str, object | None], query: str) -> bool:
    if not query.strip():
        return True
    q = query.strip().lower()
    return any(q in str(value).lower() for value in row.values() if value is not None)


def _missing_match(value: object | None, only_missing: bool) -> bool:
    if not only_missing:
        return True
    return value is None


def _typed_number(value: object | None) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value))
    except ValueError:
        return None


def _to_hashable_row(row: dict[str, object | None], fieldnames: list[str]) -> tuple[object | None, ...]:
    return tuple(row.get(field) for field in fieldnames)


def _count_outliers(values: list[float]) -> int:
    if len(values) < 4:
        return 0
    sorted_values = sorted(values)
    q1 = sorted_values[int(len(sorted_values) * 0.25)]
    q3 = sorted_values[int(len(sorted_values) * 0.75)]
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    high = q3 + 1.5 * iqr
    return sum(1 for value in sorted_values if value < low or value > high)


@app.post("/api/datasets/generate", response_model=DatasetSummaryResponse)
def generate_dataset(payload: DatasetGenerateRequest) -> DatasetSummaryResponse:
    bundle = generate_dataset_bundle(
        dataset=payload.dataset,
        n=payload.num_records,
        include_missing_values=payload.include_missing_values,
        include_outliers=payload.include_outliers,
        difficulty=payload.difficulty,
    )
    dataset_id = uuid4().hex
    csv_path = GENERATED_DIR / f"{dataset_id}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=bundle.fieldnames)
        writer.writeheader()
        writer.writerows(bundle.rows)

    save_dataset_record(
        dataset_id=dataset_id,
        dataset_name=payload.dataset,
        csv_path=csv_path,
        rows_count=len(bundle.rows),
        columns_count=len(bundle.fieldnames),
        difficulty=payload.difficulty,
        include_missing_values=payload.include_missing_values,
        include_outliers=payload.include_outliers,
    )

    return _build_summary(
        dataset_id,
        payload.dataset,
        payload.difficulty,
        bundle.fieldnames,
        bundle.rows,
    )


@app.get("/api/datasets/{dataset_id}", response_model=DatasetSummaryResponse)
def get_dataset_summary(dataset_id: str) -> DatasetSummaryResponse:
    row = get_dataset_record(dataset_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    csv_path = Path(row["csv_path"])
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="Dataset file missing")

    fieldnames, rows = _load_rows(csv_path)
    return _build_summary(dataset_id, row["dataset_name"], row["difficulty"], fieldnames, rows)


@app.get("/api/datasets/{dataset_id}/rows")
def get_dataset_rows(dataset_id: str) -> dict[str, object]:
    row = get_dataset_record(dataset_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    csv_path = Path(row["csv_path"])
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="Dataset file missing")

    _, rows = _load_rows(csv_path)
    return {"dataset_id": dataset_id, "rows": rows}


@app.get("/api/datasets/{dataset_id}/rows/paginated", response_model=PaginatedRowsResponse)
def get_dataset_rows_paginated(
    dataset_id: str,
    page: int = 1,
    page_size: int = 50,
    search: str = "",
    sort_by: str = "",
    sort_dir: str = "asc",
    filter_column: str = "",
    filter_value: str = "",
    numeric_min: float | None = None,
    numeric_max: float | None = None,
    missing_only: bool = False,
) -> PaginatedRowsResponse:
    if page < 1:
        raise HTTPException(status_code=422, detail="page must be >= 1")
    if page_size < 1 or page_size > 200:
        raise HTTPException(status_code=422, detail="page_size must be between 1 and 200")
    if sort_dir not in {"asc", "desc"}:
        raise HTTPException(status_code=422, detail="sort_dir must be asc or desc")

    row = get_dataset_record(dataset_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    csv_path = Path(row["csv_path"])
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="Dataset file missing")

    fieldnames, rows = _load_rows(csv_path)
    filtered: list[dict[str, object | None]] = []
    for item in rows:
        if not _search_match(item, search):
            continue
        if filter_column:
            if filter_column not in fieldnames:
                raise HTTPException(status_code=422, detail=f"Unknown filter_column: {filter_column}")
            target = item.get(filter_column)
            if not _missing_match(target, missing_only):
                continue
            if filter_value and target is not None and filter_value.lower() not in str(target).lower():
                continue
            if numeric_min is not None or numeric_max is not None:
                num = _typed_number(target)
                if num is None:
                    continue
                if numeric_min is not None and num < numeric_min:
                    continue
                if numeric_max is not None and num > numeric_max:
                    continue
        filtered.append(item)

    if sort_by:
        if sort_by not in fieldnames:
            raise HTTPException(status_code=422, detail=f"Unknown sort_by column: {sort_by}")

        def sort_key(item: dict[str, object | None]) -> tuple[int, object]:
            value = item.get(sort_by)
            if value is None:
                return (1, "")
            numeric_value = _typed_number(value)
            if numeric_value is not None:
                return (0, numeric_value)
            return (0, str(value).lower())

        filtered.sort(key=sort_key, reverse=(sort_dir == "desc"))

    total_rows = len(filtered)
    total_pages = max(1, math.ceil(total_rows / page_size))
    start = (page - 1) * page_size
    end = start + page_size
    page_rows = filtered[start:end]

    return PaginatedRowsResponse(
        dataset_id=dataset_id,
        page=page,
        page_size=page_size,
        total_rows=total_rows,
        total_pages=total_pages,
        rows=page_rows,
    )


@app.get("/api/datasets/{dataset_id}/profile", response_model=DatasetProfileResponse)
def get_dataset_profile(dataset_id: str) -> DatasetProfileResponse:
    row = get_dataset_record(dataset_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    csv_path = Path(row["csv_path"])
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="Dataset file missing")

    fieldnames, rows = _load_rows(csv_path)
    columns_map: dict[str, list[object | None]] = {name: [] for name in fieldnames}
    row_seen: set[tuple[object | None, ...]] = set()
    duplicate_rows = 0
    missing_cells = 0

    for item in rows:
        row_tuple = _to_hashable_row(item, fieldnames)
        if row_tuple in row_seen:
            duplicate_rows += 1
        else:
            row_seen.add(row_tuple)

        for col in fieldnames:
            value = item.get(col)
            columns_map[col].append(value)
            if value is None:
                missing_cells += 1

    numeric_columns: list[str] = []
    categorical_columns: list[str] = []
    outlier_counts: dict[str, int] = {}
    numeric_stats: dict[str, NumericStats] = {}

    for col, values in columns_map.items():
        nums = [_typed_number(v) for v in values]
        numeric_values = [v for v in nums if v is not None]
        if len(numeric_values) == 0:
            categorical_columns.append(col)
            continue

        numeric_columns.append(col)
        outlier_counts[col] = _count_outliers(numeric_values)
        if len(numeric_values) == 1:
            std_dev = 0.0
        else:
            std_dev = float(statistics.stdev(numeric_values))
        numeric_stats[col] = NumericStats(
            count=len(numeric_values),
            mean=round(float(statistics.mean(numeric_values)), 4),
            median=round(float(statistics.median(numeric_values)), 4),
            min=round(float(min(numeric_values)), 4),
            max=round(float(max(numeric_values)), 4),
            std_dev=round(std_dev, 4),
        )

    return DatasetProfileResponse(
        dataset_id=dataset_id,
        rows=len(rows),
        columns=len(fieldnames),
        missing_cells=missing_cells,
        duplicate_rows=duplicate_rows,
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        outlier_counts=outlier_counts,
        numeric_stats=numeric_stats,
    )


@app.get("/api/datasets/{dataset_id}/download")
def download_dataset(dataset_id: str) -> FileResponse:
    row = get_dataset_record(dataset_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    csv_path = Path(row["csv_path"])
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="Dataset file missing")

    return FileResponse(path=csv_path, media_type="text/csv", filename=f"{row['dataset_name']}_{dataset_id}.csv")


@app.delete("/api/datasets/{dataset_id}")
def reset_dataset(dataset_id: str) -> dict[str, str]:
    row = get_dataset_record(dataset_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    csv_path = Path(row["csv_path"])
    if csv_path.exists():
        csv_path.unlink()

    delete_dataset_record(dataset_id)
    return {"status": "deleted"}


@app.get("/", include_in_schema=False, response_model=None)
def serve_root() -> FileResponse | JSONResponse:
    index_file = FRONTEND_DIST_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return JSONResponse(
        status_code=200,
        content={
            "message": "DataScience Lab API is running.",
            "hint": "Build frontend/dist to serve UI from this backend root.",
        },
    )


@app.get("/{full_path:path}", include_in_schema=False, response_model=None)
def serve_spa_files(full_path: str) -> FileResponse | JSONResponse:
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not found")

    dist_root = FRONTEND_DIST_DIR.resolve()
    candidate_path = (dist_root / full_path).resolve()
    if candidate_path.exists() and candidate_path.is_file() and candidate_path.is_relative_to(dist_root):
        return FileResponse(candidate_path)

    index_file = dist_root / "index.html"
    if index_file.exists():
        return FileResponse(index_file)

    return JSONResponse(
        status_code=404,
        content={
            "detail": "Frontend build artifacts not found. Build frontend first.",
        },
    )
