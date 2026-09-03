from typing import Literal

from pydantic import BaseModel, Field


class DatasetGenerateRequest(BaseModel):
    dataset: Literal[
        "student_performance",
        "house_prices",
        "customer_churn",
        "movie_success",
        "retail_sales",
        "environmental_data",
    ] = "student_performance"
    num_records: int = Field(default=500, ge=100, le=5000)
    include_missing_values: bool = True
    include_outliers: bool = True
    difficulty: Literal["beginner", "intermediate", "advanced"] = "beginner"


class DatasetSummaryResponse(BaseModel):
    dataset_id: str
    dataset_name: str
    rows: int
    columns: int
    target_suggestion: str
    difficulty: str
    column_descriptions: dict[str, str]
    data_types: dict[str, str]
    missing_summary: dict[str, int]
    preview: list[dict]
    suggested_questions: list[str]


class DatasetRecordResponse(BaseModel):
    dataset_id: str
    dataset_name: str
    rows_count: int
    columns_count: int
    difficulty: str
    include_missing_values: bool
    include_outliers: bool
    created_at: str


class PaginatedRowsResponse(BaseModel):
    dataset_id: str
    page: int
    page_size: int
    total_rows: int
    total_pages: int
    rows: list[dict]


class NumericStats(BaseModel):
    count: int
    mean: float
    median: float
    min: float
    max: float
    std_dev: float


class DatasetProfileResponse(BaseModel):
    dataset_id: str
    rows: int
    columns: int
    missing_cells: int
    duplicate_rows: int
    numeric_columns: list[str]
    categorical_columns: list[str]
    outlier_counts: dict[str, int]
    numeric_stats: dict[str, NumericStats]
