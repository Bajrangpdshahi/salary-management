"""Phase 6 — Seed Script (Performance Focus)

Bulk inserts 10,000 employees using SQLAlchemy Core `executemany` for performance.
- WAL journal mode + NORMAL synchronous for speed
- Idempotency: skips if >= N employees already exist
- Target: < 3 seconds for 10,000 records

Usage (run from `backend/` directory):
    python scripts/seed.py                  # seed 10,000 (default)
    python scripts/seed.py --count 5000     # seed 5,000
    python scripts/seed.py -c 100           # seed 100 (quick test)
    python scripts/seed.py -c 50000         # seed 50,000 (load testing)

Resetting (delete DB first, then re-seed):
    del app\\salary_management.db && python scripts/seed.py       # Windows
    rm app/salary_management.db && python scripts/seed.py         # macOS/Linux

Idempotency note:
    If the DB already has >= target employees, the script skips with:
    "Already have NNN employees (target: NNN). Skipping seed."
    Delete the DB file first (see above) if you need to re-seed with the same count.
"""

import os
import sys
import time
import random
import argparse
from pathlib import Path
from datetime import date, timedelta

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Ensure the backend directory is on sys.path so `from app.…` imports resolve
# regardless of whether the script is invoked as `python scripts/seed.py` or
# `python -m scripts.seed`.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Deterministic path — matches backend/app/database.py
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "app", "salary_management.db",
)
DATABASE_URL = f"sqlite:///{DB_PATH}"
BATCH_SIZE = 1000

COUNTRIES = [
    "India", "USA", "UK", "Germany", "Canada", "Australia",
    "Singapore", "Brazil", "France", "Japan",
]

JOB_TITLES = [
    "Software Engineer", "Senior Software Engineer", "Staff Engineer",
    "Principal Engineer", "Engineering Manager", "Product Manager",
    "Data Analyst", "Data Scientist", "DevOps Engineer", "QA Engineer",
    "UI/UX Designer", "Technical Lead", "HR Business Partner",
    "Finance Analyst", "Marketing Manager", "Sales Executive",
]

DEPARTMENTS = [
    "Engineering", "Product", "Data", "Operations",
    "Marketing", "Sales", "HR", "Finance", "Design",
]

SALARY_RANGE = {
    "Software Engineer": (60000, 100000),
    "Senior Software Engineer": (90000, 140000),
    "Staff Engineer": (130000, 180000),
    "Principal Engineer": (160000, 220000),
    "Engineering Manager": (140000, 200000),
    "Product Manager": (110000, 160000),
    "Data Analyst": (55000, 85000),
    "Data Scientist": (90000, 140000),
    "DevOps Engineer": (80000, 130000),
    "QA Engineer": (55000, 95000),
    "UI/UX Designer": (60000, 100000),
    "Technical Lead": (120000, 170000),
    "HR Business Partner": (50000, 85000),
    "Finance Analyst": (55000, 90000),
    "Marketing Manager": (65000, 110000),
    "Sales Executive": (50000, 95000),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_names(filepath: str) -> list[str]:
    """Load name list from file, splitting on commas and newlines."""
    raw = Path(filepath).read_text().strip()
    return [name.strip() for name in raw.replace("\n", ",").split(",") if name.strip()]


def generate_employee(first_names: list[str], last_names: list[str]) -> dict:
    """Generate a single random employee record."""
    job_title = random.choice(JOB_TITLES)
    salary_min, salary_max = SALARY_RANGE[job_title]
    hire_date = date.today() - timedelta(days=random.randint(30, 3650))
    return {
        "full_name": f"{random.choice(first_names)} {random.choice(last_names)}",
        "job_title": job_title,
        "department": random.choice(DEPARTMENTS),
        "country": random.choice(COUNTRIES),
        "salary": round(random.uniform(salary_min, salary_max), 2),
        "currency": "USD",
        "employment_type": random.choice(
            ["Full-time", "Full-time", "Full-time", "Contractor"]
        ),
        "hire_date": hire_date.isoformat(),
        "is_active": True,
    }


# ---------------------------------------------------------------------------
# Main seeder
# ---------------------------------------------------------------------------
def seed(n: int = 10000):
    """Seed the database with `n` employee records."""
    engine = create_engine(DATABASE_URL)

    # --- Idempotency check ---
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM employees")).scalar()
        if count >= n:
            print(f"Already have {count} employees (target: {n}). Skipping seed.")
            return

    # --- Enable WAL mode for faster writes ---
    with engine.connect() as conn:
        conn.execute(text("PRAGMA journal_mode=WAL"))
        conn.execute(text("PRAGMA synchronous=NORMAL"))
        # Ensure table exists
        from app.models.employee import Employee  # noqa: F401
        from app.database import Base
        Base.metadata.create_all(bind=engine)

    print(f"Seeding {n} employees...")
    first_names = load_names("scripts/first_names.txt")
    last_names = load_names("scripts/last_names.txt")

    employees = [generate_employee(first_names, last_names) for _ in range(n)]

    start = time.perf_counter()
    with engine.begin() as conn:
        for i in range(0, len(employees), BATCH_SIZE):
            batch = employees[i:i + BATCH_SIZE]
            conn.execute(
                text("""
                    INSERT INTO employees
                    (full_name, job_title, department, country, salary,
                     currency, employment_type, hire_date, is_active)
                    VALUES
                    (:full_name, :job_title, :department, :country, :salary,
                     :currency, :employment_type, :hire_date, :is_active)
                """),
                batch,
            )
    elapsed = time.perf_counter() - start
    print(
        f"[OK] Seeded {n} employees in {elapsed:.2f}s "
        f"({n / elapsed:.0f} records/sec)"
    )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Seed the salary_management.db with employee data"
    )
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=10000,
        help="Number of employees to seed (default: 10000)",
    )
    args = parser.parse_args()
    seed(args.count)