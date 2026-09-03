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
