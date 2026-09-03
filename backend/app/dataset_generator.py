from __future__ import annotations

from dataclasses import dataclass
import random

@dataclass(frozen=True)
class DatasetBundle:
    rows: list[dict[str, object | None]]
    fieldnames: list[str]
    column_descriptions: dict[str, str]
    target_suggestion: str
    suggested_questions: list[str]


def generate_student_dataset(
    n: int = 500,
    include_missing_values: bool = True,
    include_outliers: bool = True,
    difficulty: str = "beginner",
    seed: int | None = None,
) -> DatasetBundle:
    rng = random.Random(seed)

    fieldnames = [
        "student_id",
        "age",
        "gender",
        "study_hours",
        "attendance",
        "sleep_hours",
        "previous_score",
        "extracurricular",
        "internet_access",
        "parent_education",
        "final_score",
    ]

    def weighted_choice(options: list[str], weights: list[float]) -> str:
        return rng.choices(options, weights=weights, k=1)[0]

    def clamp(value: float, low: float, high: float) -> float:
        return max(low, min(high, value))

    parent_education_boost = {
        "high_school": -1.0,
        "diploma": 0.3,
        "graduate": 1.5,
        "postgraduate": 2.4,
    }
    internet_boost = {"good": 1.8, "limited": -0.8, "none": -2.1}
    extracurricular_boost = {"yes": 1.4, "no": -0.4}

    noise_scale = {"beginner": 5.5, "intermediate": 7.0, "advanced": 8.5}.get(difficulty, 6.0)

    rows: list[dict[str, object | None]] = []
    for idx in range(1, n + 1):
        age = rng.randint(16, 19)
        gender = weighted_choice(["female", "male", "non-binary"], [0.47, 0.47, 0.06])
        study_hours = round(clamp(rng.gauss(4.8, 1.7), 0.3, 11.5), 2)
        attendance = round(clamp(rng.gauss(84, 11.5), 45, 100), 1)
        sleep_hours = round(clamp(rng.gauss(7.1, 1.0), 4.0, 10.0), 2)
        previous_score = round(clamp(rng.gauss(72, 13), 30, 99), 1)
        extracurricular = weighted_choice(["yes", "no"], [0.58, 0.42])
        internet_access = weighted_choice(["good", "limited", "none"], [0.71, 0.23, 0.06])
        parent_education = weighted_choice(
            ["high_school", "diploma", "graduate", "postgraduate"],
            [0.35, 0.26, 0.25, 0.14],
        )
        noise = rng.gauss(0, noise_scale)
        final_score = (
            0.34 * previous_score
            + 3.2 * study_hours
            + 0.22 * attendance
            + 1.3 * sleep_hours
            + parent_education_boost[parent_education]
            + internet_boost[internet_access]
            + extracurricular_boost[extracurricular]
            + noise
        )
        final_score = round(clamp(final_score, 32, 100), 1)

        rows.append(
            {
                "student_id": idx,
                "age": age,
                "gender": gender,
                "study_hours": study_hours,
                "attendance": attendance,
                "sleep_hours": sleep_hours,
                "previous_score": previous_score,
                "extracurricular": extracurricular,
                "internet_access": internet_access,
                "parent_education": parent_education,
                "final_score": final_score,
            }
        )

    if include_outliers and n > 25:
        outlier_count = max(5, int(0.02 * n))
        for i in rng.sample(range(n), outlier_count):
            rows[i]["study_hours"] = round(rng.uniform(0.3, 12.0), 2)
            rows[i]["attendance"] = round(rng.uniform(30, 100), 1)
            base = float(rows[i]["final_score"])
            rows[i]["final_score"] = round(clamp(base + rng.gauss(0, 18), 15, 100), 1)

    if include_missing_values:
        missing_plan = {
            "study_hours": 0.03,
            "attendance": 0.025,
            "sleep_hours": 0.02,
            "previous_score": 0.03,
            "internet_access": 0.02,
            "parent_education": 0.015,
        }
        for col, frac in missing_plan.items():
            m_count = max(1, int(frac * n))
            for i in rng.sample(range(n), m_count):
                rows[i][col] = None

    column_descriptions = {
        "student_id": "Unique identifier for each student.",
        "age": "Age in years.",
        "gender": "Student gender category.",
        "study_hours": "Average self-study hours per day.",
        "attendance": "Class attendance percentage.",
        "sleep_hours": "Average sleep hours per day.",
        "previous_score": "Previous exam score out of 100.",
        "extracurricular": "Whether the student participates in extracurricular activities.",
        "internet_access": "Quality of internet access at home.",
        "parent_education": "Highest parent/guardian education level.",
        "final_score": "Current final score out of 100 (target variable).",
    }

    suggested_questions = [
        "How does attendance relate to final_score?",
        "Which parent_education group has the highest average final_score?",
        "Do students with higher study_hours usually score better?",
        "Which columns contain missing values and how should we handle them?",
        "Are there outliers in study_hours or final_score?",
    ]

    return DatasetBundle(
        rows=rows,
        fieldnames=fieldnames,
        column_descriptions=column_descriptions,
        target_suggestion="final_score",
        suggested_questions=suggested_questions,
    )
