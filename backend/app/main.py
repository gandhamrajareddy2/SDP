from __future__ import annotations

import csv
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .config import GENERATED_DIR
from .dataset_generator import generate_student_dataset
from .db import delete_dataset_record, get_dataset_record, init_db, save_dataset_record
from .schemas import DatasetGenerateRequest, DatasetSummaryResponse

app = FastAPI(title="DataScience Lab API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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
    return [
        {
            "id": "student_performance",
            "title": "Student Performance",
            "description": "Predict student final performance using study patterns.",
        },
        {
            "id": "house_prices",
            "title": "House Prices",
            "description": "Analyze and predict house prices.",
        },
        {
            "id": "customer_churn",
            "title": "Customer Churn",
            "description": "Understand why customers leave.",
        },
        {
            "id": "movie_success",
            "title": "Movie Success",
            "description": "Analyze factors associated with movie success.",
        },
        {
            "id": "retail_sales",
            "title": "Retail Sales",
            "description": "Analyze sales patterns and forecast outcomes.",
        },
        {
            "id": "environmental_data",
            "title": "Environmental Data",
            "description": "Analyze temperature, rainfall, and pollution trends.",
        },
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
    cols_by_name: dict[str, list[object | None]] = {column: [] for column in fieldnames}
    for row in rows:
        for column in fieldnames:
            cols_by_name[column].append(row.get(column))

    return DatasetSummaryResponse(
        dataset_id=dataset_id,
        dataset_name=dataset_name,
        rows=len(rows),
        columns=len(fieldnames),
        target_suggestion="final_score",
        difficulty=difficulty,
        column_descriptions={
            "student_id": "Unique identifier for each student.",
            "age": "Age in years.",
            "gender": "Student gender category.",
            "study_hours": "Average self-study hours per day.",
            "attendance": "Class attendance percentage.",
            "sleep_hours": "Average sleep hours per day.",
            "previous_score": "Previous exam score out of 100.",
            "extracurricular": "Whether student participates in extracurricular activities.",
            "internet_access": "Quality of internet access at home.",
            "parent_education": "Highest parent/guardian education level.",
            "final_score": "Current final score out of 100 (target variable).",
        },
        data_types={column: _infer_dtype(values) for column, values in cols_by_name.items()},
        missing_summary={
            column: sum(1 for value in values if value is None)
            for column, values in cols_by_name.items()
        },
        preview=rows[:20],
        suggested_questions=[
            "How does attendance relate to final_score?",
            "Which parent_education group has the highest average final_score?",
            "Do students with higher study_hours usually score better?",
            "Which columns contain missing values and how should we handle them?",
            "Are there outliers in study_hours or final_score?",
        ],
    )


@app.post("/api/datasets/generate", response_model=DatasetSummaryResponse)
def generate_dataset(payload: DatasetGenerateRequest) -> DatasetSummaryResponse:
    if payload.dataset != "student_performance":
        raise HTTPException(status_code=400, detail="Only student_performance is supported in this slice.")

    bundle = generate_student_dataset(
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
