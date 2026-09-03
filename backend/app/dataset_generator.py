from __future__ import annotations

from dataclasses import dataclass
import random


PROJECTS: list[dict[str, str]] = [
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
        "description": "Analyze sales patterns and predict outcomes.",
    },
    {
        "id": "environmental_data",
        "title": "Environmental Data",
        "description": "Analyze temperature, rainfall, and pollution trends.",
    },
]

@dataclass(frozen=True)
class DatasetBundle:
    rows: list[dict[str, object | None]]
    fieldnames: list[str]
    column_descriptions: dict[str, str]
    target_suggestion: str
    suggested_questions: list[str]


def _weighted_choice(rng: random.Random, options: list[str], weights: list[float]) -> str:
    return rng.choices(options, weights=weights, k=1)[0]


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _apply_missing_values(
    rows: list[dict[str, object | None]],
    n: int,
    rng: random.Random,
    missing_plan: dict[str, float],
) -> None:
    for col, frac in missing_plan.items():
        m_count = max(1, int(frac * n))
        for i in rng.sample(range(n), m_count):
            rows[i][col] = None


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
        gender = _weighted_choice(rng, ["female", "male", "non-binary"], [0.47, 0.47, 0.06])
        study_hours = round(_clamp(rng.gauss(4.8, 1.7), 0.3, 11.5), 2)
        attendance = round(_clamp(rng.gauss(84, 11.5), 45, 100), 1)
        sleep_hours = round(_clamp(rng.gauss(7.1, 1.0), 4.0, 10.0), 2)
        previous_score = round(_clamp(rng.gauss(72, 13), 30, 99), 1)
        extracurricular = _weighted_choice(rng, ["yes", "no"], [0.58, 0.42])
        internet_access = _weighted_choice(rng, ["good", "limited", "none"], [0.71, 0.23, 0.06])
        parent_education = _weighted_choice(
            rng,
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
        final_score = round(_clamp(final_score, 32, 100), 1)

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
            rows[i]["final_score"] = round(_clamp(base + rng.gauss(0, 18), 15, 100), 1)

    if include_missing_values:
        _apply_missing_values(
            rows,
            n,
            rng,
            {
                "study_hours": 0.03,
                "attendance": 0.025,
                "sleep_hours": 0.02,
                "previous_score": 0.03,
                "internet_access": 0.02,
                "parent_education": 0.015,
            },
        )

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


def generate_house_prices_dataset(
    n: int,
    include_missing_values: bool,
    include_outliers: bool,
    difficulty: str,
    seed: int | None,
) -> DatasetBundle:
    rng = random.Random(seed)
    fieldnames = [
        "house_id",
        "area_sqft",
        "bedrooms",
        "bathrooms",
        "age_years",
        "location_tier",
        "nearby_school_rating",
        "crime_index",
        "has_garage",
        "price_lakh",
    ]

    location_boost = {"urban": 45, "suburban": 20, "rural": -6}
    garage_boost = {"yes": 8, "no": -3}
    noise_scale = {"beginner": 8.0, "intermediate": 12.0, "advanced": 16.0}.get(difficulty, 10.0)

    rows: list[dict[str, object | None]] = []
    for idx in range(1, n + 1):
        area = round(_clamp(rng.gauss(1450, 460), 420, 4200), 1)
        bedrooms = rng.randint(1, 6)
        bathrooms = _clamp(bedrooms - 1 + rng.randint(0, 2), 1, 4)
        age = rng.randint(0, 45)
        location = _weighted_choice(rng, ["urban", "suburban", "rural"], [0.34, 0.44, 0.22])
        school = round(_clamp(rng.gauss(7.1, 1.5), 1, 10), 1)
        crime = round(_clamp(rng.gauss(4.5, 2.0), 0.2, 10), 1)
        garage = _weighted_choice(rng, ["yes", "no"], [0.64, 0.36])

        price = (
            0.043 * area
            + 7.6 * bedrooms
            + 6.4 * float(bathrooms)
            - 0.26 * age
            + location_boost[location]
            + 2.2 * school
            - 1.35 * crime
            + garage_boost[garage]
            + rng.gauss(0, noise_scale)
        )
        price = round(_clamp(price, 18, 460), 1)

        rows.append(
            {
                "house_id": idx,
                "area_sqft": area,
                "bedrooms": bedrooms,
                "bathrooms": float(bathrooms),
                "age_years": age,
                "location_tier": location,
                "nearby_school_rating": school,
                "crime_index": crime,
                "has_garage": garage,
                "price_lakh": price,
            }
        )

    if include_outliers and n > 20:
        for i in rng.sample(range(n), max(4, int(0.02 * n))):
            rows[i]["area_sqft"] = round(_clamp(float(rows[i]["area_sqft"]) * rng.uniform(1.4, 1.9), 500, 5600), 1)
            rows[i]["price_lakh"] = round(_clamp(float(rows[i]["price_lakh"]) + rng.gauss(0, 70), 15, 520), 1)

    if include_missing_values:
        _apply_missing_values(
            rows,
            n,
            rng,
            {"nearby_school_rating": 0.03, "crime_index": 0.02, "has_garage": 0.015, "bathrooms": 0.02},
        )

    return DatasetBundle(
        rows=rows,
        fieldnames=fieldnames,
        column_descriptions={
            "house_id": "Unique house identifier.",
            "area_sqft": "Built-up area in square feet.",
            "bedrooms": "Number of bedrooms.",
            "bathrooms": "Number of bathrooms.",
            "age_years": "Age of property in years.",
            "location_tier": "Area category.",
            "nearby_school_rating": "Average nearby school rating (1 to 10).",
            "crime_index": "Crime index score (higher means riskier).",
            "has_garage": "Garage availability.",
            "price_lakh": "Estimated house price in lakhs.",
        },
        target_suggestion="price_lakh",
        suggested_questions=[
            "How does area_sqft relate to price_lakh?",
            "Which location_tier has the highest average price_lakh?",
            "Does crime_index appear inversely related to price?",
            "How should missing school/crime values be handled?",
            "Are there outliers in area_sqft and price_lakh?",
        ],
    )


def generate_customer_churn_dataset(
    n: int,
    include_missing_values: bool,
    include_outliers: bool,
    difficulty: str,
    seed: int | None,
) -> DatasetBundle:
    rng = random.Random(seed)
    fieldnames = [
        "customer_id",
        "tenure_months",
        "monthly_charges",
        "contract_type",
        "support_tickets",
        "payment_delay_days",
        "internet_quality",
        "uses_auto_pay",
        "churn",
    ]
    rows: list[dict[str, object | None]] = []

    for idx in range(1, n + 1):
        tenure = rng.randint(1, 72)
        monthly = round(_clamp(rng.gauss(64, 18), 18, 180), 2)
        contract = _weighted_choice(rng, ["month_to_month", "one_year", "two_year"], [0.54, 0.27, 0.19])
        tickets = max(0, int(round(rng.gauss(2.1, 1.8))))
        delay = max(0, int(round(rng.gauss(3.8, 3.5))))
        quality = _weighted_choice(rng, ["good", "average", "poor"], [0.57, 0.31, 0.12])
        auto_pay = _weighted_choice(rng, ["yes", "no"], [0.62, 0.38])

        risk = 0.12
        risk += 0.015 * max(0, monthly - 60)
        risk += 0.018 * tickets
        risk += 0.01 * delay
        risk += 0.22 if contract == "month_to_month" else (0.08 if contract == "one_year" else -0.03)
        risk += 0.17 if quality == "poor" else (0.04 if quality == "average" else -0.05)
        risk += 0.1 if auto_pay == "no" else -0.05
        risk -= 0.0026 * tenure
        risk += rng.gauss(0, {"beginner": 0.05, "intermediate": 0.08, "advanced": 0.11}.get(difficulty, 0.07))
        churn = "yes" if rng.random() < _clamp(risk, 0.03, 0.92) else "no"

        rows.append(
            {
                "customer_id": idx,
                "tenure_months": tenure,
                "monthly_charges": monthly,
                "contract_type": contract,
                "support_tickets": tickets,
                "payment_delay_days": delay,
                "internet_quality": quality,
                "uses_auto_pay": auto_pay,
                "churn": churn,
            }
        )

    if include_outliers and n > 20:
        for i in rng.sample(range(n), max(4, int(0.02 * n))):
            rows[i]["monthly_charges"] = round(_clamp(float(rows[i]["monthly_charges"]) * rng.uniform(1.4, 1.9), 25, 250), 2)
            rows[i]["payment_delay_days"] = int(_clamp(float(rows[i]["payment_delay_days"]) + rng.uniform(15, 45), 0, 75))

    if include_missing_values:
        _apply_missing_values(
            rows,
            n,
            rng,
            {"internet_quality": 0.02, "uses_auto_pay": 0.015, "monthly_charges": 0.015},
        )

    return DatasetBundle(
        rows=rows,
        fieldnames=fieldnames,
        column_descriptions={
            "customer_id": "Unique customer identifier.",
            "tenure_months": "Months the customer has stayed.",
            "monthly_charges": "Monthly bill amount.",
            "contract_type": "Plan contract duration.",
            "support_tickets": "Number of support tickets raised.",
            "payment_delay_days": "Average delay in bill payment (days).",
            "internet_quality": "Perceived internet quality.",
            "uses_auto_pay": "Whether auto payment is enabled.",
            "churn": "Whether customer left the service (target).",
        },
        target_suggestion="churn",
        suggested_questions=[
            "Which contract_type has the highest churn rate?",
            "Does monthly_charges influence churn?",
            "How does tenure_months relate to churn?",
            "Do support_tickets and delay_days indicate churn risk?",
            "Which missing-value strategy is best before classification?",
        ],
    )


def generate_movie_success_dataset(
    n: int,
    include_missing_values: bool,
    include_outliers: bool,
    difficulty: str,
    seed: int | None,
) -> DatasetBundle:
    rng = random.Random(seed)
    fieldnames = [
        "movie_id",
        "budget_musd",
        "genre",
        "star_power",
        "critic_score",
        "marketing_musd",
        "release_season",
        "screens",
        "opening_weekend_musd",
        "worldwide_gross_musd",
    ]
    genre_boost = {"action": 24, "drama": 4, "comedy": 8, "sci_fi": 20, "romance": 3}
    season_boost = {"summer": 14, "winter": 10, "festival": 9, "off_season": -3}

    rows: list[dict[str, object | None]] = []
    for idx in range(1, n + 1):
        budget = round(_clamp(rng.gauss(58, 35), 8, 240), 2)
        genre = _weighted_choice(rng, ["action", "drama", "comedy", "sci_fi", "romance"], [0.24, 0.21, 0.22, 0.18, 0.15])
        star_power = round(_clamp(rng.gauss(6.2, 2.0), 1, 10), 1)
        critic = round(_clamp(rng.gauss(64, 15), 10, 98), 1)
        marketing = round(_clamp(0.36 * budget + rng.gauss(9, 6), 2, 110), 2)
        season = _weighted_choice(rng, ["summer", "winter", "festival", "off_season"], [0.31, 0.26, 0.19, 0.24])
        screens = int(_clamp(rng.gauss(1800 + budget * 15, 520), 420, 5200))

        opening = (
            0.22 * budget
            + 0.47 * marketing
            + 1.7 * star_power
            + 0.13 * critic
            + 0.0052 * screens
            + genre_boost[genre]
            + season_boost[season]
            + rng.gauss(0, {"beginner": 6.0, "intermediate": 10.0, "advanced": 14.0}.get(difficulty, 8.0))
        )
        opening = round(_clamp(opening, 2, 180), 2)
        gross = round(_clamp(2.1 * opening + 1.35 * budget + rng.gauss(0, 40), 8, 980), 2)

        rows.append(
            {
                "movie_id": idx,
                "budget_musd": budget,
                "genre": genre,
                "star_power": star_power,
                "critic_score": critic,
                "marketing_musd": marketing,
                "release_season": season,
                "screens": screens,
                "opening_weekend_musd": opening,
                "worldwide_gross_musd": gross,
            }
        )

    if include_outliers and n > 20:
        for i in rng.sample(range(n), max(4, int(0.02 * n))):
            rows[i]["worldwide_gross_musd"] = round(_clamp(float(rows[i]["worldwide_gross_musd"]) + rng.gauss(120, 65), 8, 1400), 2)

    if include_missing_values:
        _apply_missing_values(
            rows,
            n,
            rng,
            {"marketing_musd": 0.02, "critic_score": 0.015, "star_power": 0.015},
        )

    return DatasetBundle(
        rows=rows,
        fieldnames=fieldnames,
        column_descriptions={
            "movie_id": "Unique movie identifier.",
            "budget_musd": "Production budget in million USD.",
            "genre": "Primary movie genre.",
            "star_power": "Combined star cast popularity score (1 to 10).",
            "critic_score": "Average critic rating (0 to 100).",
            "marketing_musd": "Marketing spend in million USD.",
            "release_season": "Release season bucket.",
            "screens": "Initial theater screens count.",
            "opening_weekend_musd": "Opening weekend collection in million USD.",
            "worldwide_gross_musd": "Worldwide gross collection in million USD.",
        },
        target_suggestion="worldwide_gross_musd",
        suggested_questions=[
            "How does budget_musd impact worldwide_gross_musd?",
            "Which genre tends to have higher average grosses?",
            "Does critic_score strongly align with gross?",
            "How important is marketing in opening weekend?",
            "Are any films extreme outliers in revenue?",
        ],
    )


def generate_retail_sales_dataset(
    n: int,
    include_missing_values: bool,
    include_outliers: bool,
    difficulty: str,
    seed: int | None,
) -> DatasetBundle:
    rng = random.Random(seed)
    fieldnames = [
        "record_id",
        "month",
        "store_footfall",
        "ad_spend_kusd",
        "discount_pct",
        "online_share_pct",
        "holiday_flag",
        "inventory_index",
        "region",
        "sales_kusd",
    ]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    season_mult = {"Nov": 1.2, "Dec": 1.35, "Jan": 0.92, "Jun": 1.05, "Jul": 1.08}
    rows: list[dict[str, object | None]] = []

    for idx in range(1, n + 1):
        month = months[(idx - 1) % 12]
        footfall = int(_clamp(rng.gauss(1600, 520), 220, 4400))
        ad_spend = round(_clamp(rng.gauss(36, 14), 2, 120), 2)
        discount = round(_clamp(rng.gauss(14, 6), 0, 40), 1)
        online_share = round(_clamp(rng.gauss(32, 13), 3, 90), 1)
        holiday = "yes" if month in {"Nov", "Dec", "Oct"} and rng.random() < 0.75 else "no"
        inventory = round(_clamp(rng.gauss(72, 16), 20, 130), 1)
        region = _weighted_choice(rng, ["north", "south", "east", "west"], [0.27, 0.25, 0.23, 0.25])

        sales = (
            0.052 * footfall
            + 1.1 * ad_spend
            + 0.46 * discount
            + 0.24 * online_share
            + 0.35 * inventory
            + (16 if holiday == "yes" else -2)
        )
        sales *= season_mult.get(month, 1.0)
        sales += rng.gauss(0, {"beginner": 10.0, "intermediate": 14.0, "advanced": 18.0}.get(difficulty, 12.0))
        sales = round(_clamp(sales, 18, 720), 2)

        rows.append(
            {
                "record_id": idx,
                "month": month,
                "store_footfall": footfall,
                "ad_spend_kusd": ad_spend,
                "discount_pct": discount,
                "online_share_pct": online_share,
                "holiday_flag": holiday,
                "inventory_index": inventory,
                "region": region,
                "sales_kusd": sales,
            }
        )

    if include_outliers and n > 20:
        for i in rng.sample(range(n), max(4, int(0.02 * n))):
            rows[i]["sales_kusd"] = round(_clamp(float(rows[i]["sales_kusd"]) + rng.gauss(95, 45), 15, 920), 2)

    if include_missing_values:
        _apply_missing_values(
            rows,
            n,
            rng,
            {"ad_spend_kusd": 0.02, "discount_pct": 0.02, "online_share_pct": 0.015, "inventory_index": 0.015},
        )

    return DatasetBundle(
        rows=rows,
        fieldnames=fieldnames,
        column_descriptions={
            "record_id": "Sales record identifier.",
            "month": "Calendar month.",
            "store_footfall": "Number of in-store visitors.",
            "ad_spend_kusd": "Ad spend in thousand USD.",
            "discount_pct": "Average discount percentage.",
            "online_share_pct": "Percent of sales coming from online channel.",
            "holiday_flag": "Whether a holiday campaign period is active.",
            "inventory_index": "Relative inventory availability score.",
            "region": "Store region.",
            "sales_kusd": "Total sales in thousand USD (target).",
        },
        target_suggestion="sales_kusd",
        suggested_questions=[
            "How does ad_spend_kusd affect sales_kusd?",
            "Which months perform best and worst?",
            "Do discount_pct and online_share_pct move sales together?",
            "Is holiday season clearly visible in sales?",
            "Are there unusual spikes in sales?",
        ],
    )


def generate_environmental_dataset(
    n: int,
    include_missing_values: bool,
    include_outliers: bool,
    difficulty: str,
    seed: int | None,
) -> DatasetBundle:
    rng = random.Random(seed)
    fieldnames = [
        "station_id",
        "month",
        "temperature_c",
        "rainfall_mm",
        "pm25",
        "humidity_pct",
        "wind_kmph",
        "green_cover_pct",
        "traffic_index",
        "air_quality_index",
    ]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_temp_shift = {"Jan": -6, "Feb": -4, "Mar": 0, "Apr": 4, "May": 7, "Jun": 9, "Jul": 8, "Aug": 7, "Sep": 4, "Oct": 0, "Nov": -3, "Dec": -5}
    rows: list[dict[str, object | None]] = []

    for idx in range(1, n + 1):
        month = months[(idx - 1) % 12]
        temp = round(_clamp(rng.gauss(24 + month_temp_shift[month], 4.2), 4, 43), 1)
        rain = round(_clamp(rng.gauss(85 if month in {"Jun", "Jul", "Aug", "Sep"} else 28, 40), 0, 280), 1)
        pm25 = round(_clamp(rng.gauss(52, 18), 8, 210), 1)
        humidity = round(_clamp(rng.gauss(61, 15), 18, 97), 1)
        wind = round(_clamp(rng.gauss(14, 5), 2, 42), 1)
        green = round(_clamp(rng.gauss(36, 15), 5, 88), 1)
        traffic = round(_clamp(rng.gauss(58, 17), 6, 100), 1)

        aqi = (
            0.95 * pm25
            + 0.35 * traffic
            + 0.18 * humidity
            - 0.22 * wind
            - 0.28 * green
            + 0.03 * temp
            + rng.gauss(0, {"beginner": 7.0, "intermediate": 10.0, "advanced": 14.0}.get(difficulty, 9.0))
        )
        aqi = round(_clamp(aqi, 25, 420), 1)

        rows.append(
            {
                "station_id": idx,
                "month": month,
                "temperature_c": temp,
                "rainfall_mm": rain,
                "pm25": pm25,
                "humidity_pct": humidity,
                "wind_kmph": wind,
                "green_cover_pct": green,
                "traffic_index": traffic,
                "air_quality_index": aqi,
            }
        )

    if include_outliers and n > 20:
        for i in rng.sample(range(n), max(4, int(0.02 * n))):
            rows[i]["pm25"] = round(_clamp(float(rows[i]["pm25"]) + rng.uniform(45, 130), 8, 310), 1)
            rows[i]["air_quality_index"] = round(_clamp(float(rows[i]["air_quality_index"]) + rng.uniform(40, 140), 20, 500), 1)

    if include_missing_values:
        _apply_missing_values(
            rows,
            n,
            rng,
            {"pm25": 0.02, "humidity_pct": 0.02, "wind_kmph": 0.015, "green_cover_pct": 0.015},
        )

    return DatasetBundle(
        rows=rows,
        fieldnames=fieldnames,
        column_descriptions={
            "station_id": "Monitoring station identifier.",
            "month": "Calendar month.",
            "temperature_c": "Average temperature in degree Celsius.",
            "rainfall_mm": "Monthly rainfall in mm.",
            "pm25": "Fine particulate matter concentration.",
            "humidity_pct": "Relative humidity percentage.",
            "wind_kmph": "Average wind speed in km/h.",
            "green_cover_pct": "Estimated green cover percentage.",
            "traffic_index": "Traffic intensity index.",
            "air_quality_index": "Air quality index (higher is poorer).",
        },
        target_suggestion="air_quality_index",
        suggested_questions=[
            "How does pm25 relate to air_quality_index?",
            "Does more green_cover_pct reduce pollution index?",
            "Which months show better or worse AQI?",
            "How does traffic_index impact AQI?",
            "Are there extreme pollution outliers?",
        ],
    )


def generate_dataset(
    dataset: str,
    n: int,
    include_missing_values: bool,
    include_outliers: bool,
    difficulty: str,
    seed: int | None = None,
) -> DatasetBundle:
    if dataset == "student_performance":
        return generate_student_dataset(n, include_missing_values, include_outliers, difficulty, seed)
    if dataset == "house_prices":
        return generate_house_prices_dataset(n, include_missing_values, include_outliers, difficulty, seed)
    if dataset == "customer_churn":
        return generate_customer_churn_dataset(n, include_missing_values, include_outliers, difficulty, seed)
    if dataset == "movie_success":
        return generate_movie_success_dataset(n, include_missing_values, include_outliers, difficulty, seed)
    if dataset == "retail_sales":
        return generate_retail_sales_dataset(n, include_missing_values, include_outliers, difficulty, seed)
    if dataset == "environmental_data":
        return generate_environmental_dataset(n, include_missing_values, include_outliers, difficulty, seed)

    raise ValueError(f"Unsupported dataset: {dataset}")


def get_projects() -> list[dict[str, str]]:
    return PROJECTS


def get_dataset_template(dataset: str) -> DatasetBundle:
    return generate_dataset(dataset, n=20, include_missing_values=False, include_outliers=False, difficulty="beginner", seed=7)
