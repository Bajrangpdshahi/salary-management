"""Phase 5 — Salary Insights Router (TDD-GREEN)

Endpoints:
  - GET /api/insights/filters              — distinct countries & job titles for dropdowns
  - GET /api/insights/country/{country}    — min/max/avg/median/percentiles/headcount
  - GET /api/insights/job-title            — stats filtered by country + job_title
  - GET /api/insights/summary              — global org-wide summary
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

from app.database import get_db
from app.models.employee import Employee

router = APIRouter(prefix="/api/insights", tags=["insights"])


def calculate_percentile(values: list[float], p: float) -> float:
    """Linear interpolation percentile calculator.

    Uses the standard (N-1)*p/100 method with linear interpolation between
    adjacent sorted values. Returns 0.0 for empty lists.
    """
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    idx = (p / 100) * (len(sorted_vals) - 1)
    lower = int(idx)
    upper = min(lower + 1, len(sorted_vals) - 1)
    return sorted_vals[lower] + (idx - lower) * (
        sorted_vals[upper] - sorted_vals[lower]
    )


# ---------------------------------------------------------------------------
# Distinct filter values for dropdowns
# ---------------------------------------------------------------------------
@router.get("/filters")
def get_filters(db: Session = Depends(get_db)):
    """Return distinct countries and job titles from active employees for dropdown population."""
    countries = (
        db.query(distinct(Employee.country))
        .filter(Employee.is_active == True, Employee.country.isnot(None))
        .order_by(Employee.country)
        .all()
    )

    job_titles = (
        db.query(distinct(Employee.job_title))
        .filter(Employee.is_active == True, Employee.job_title.isnot(None))
        .order_by(Employee.job_title)
        .all()
    )

    return {
        "countries": [row[0] for row in countries],
        "job_titles": [row[0] for row in job_titles],
    }


# ---------------------------------------------------------------------------
# Country-level stats
# ---------------------------------------------------------------------------
@router.get("/country/{country}")
def get_country_stats(country: str, db: Session = Depends(get_db)):
    """Return salary statistics for all active employees in a given country."""
    employees = (
        db.query(Employee)
        .filter(
            Employee.country == country,
            Employee.is_active == True,
        )
        .all()
    )

    if not employees:
        raise HTTPException(
            status_code=404,
            detail=f"No employees found in {country}",
        )

    salaries = [e.salary for e in employees]
    return {
        "country": country,
        "headcount": len(salaries),
        "min_salary": min(salaries),
        "max_salary": max(salaries),
        "avg_salary": sum(salaries) / len(salaries),
        "median_salary": calculate_percentile(salaries, 50),
        "p25": calculate_percentile(salaries, 25),
        "p50": calculate_percentile(salaries, 50),
        "p75": calculate_percentile(salaries, 75),
        "p90": calculate_percentile(salaries, 90),
    }


# ---------------------------------------------------------------------------
# Job-title stats (filtered by country + title)
# ---------------------------------------------------------------------------
@router.get("/job-title")
def get_job_title_stats(
    country: str = Query(...),
    job_title: str = Query(...),
    db: Session = Depends(get_db),
):
    """Return salary statistics filtered by country and job title."""
    employees = (
        db.query(Employee)
        .filter(
            Employee.country == country,
            Employee.job_title == job_title,
            Employee.is_active == True,
        )
        .all()
    )

    if not employees:
        raise HTTPException(
            status_code=404,
            detail=f"No employees with title '{job_title}' in {country}",
        )

    salaries = [e.salary for e in employees]
    return {
        "country": country,
        "job_title": job_title,
        "headcount": len(salaries),
        "min_salary": min(salaries),
        "max_salary": max(salaries),
        "avg_salary": sum(salaries) / len(salaries),
        "median_salary": calculate_percentile(salaries, 50),
    }


# ---------------------------------------------------------------------------
# Global org-wide summary
# ---------------------------------------------------------------------------
@router.get("/summary")
def get_global_summary(db: Session = Depends(get_db)):
    """Overall org-wide salary summary — useful for HR dashboard."""
    result = (
        db.query(
            func.count(Employee.id).label("total_employees"),
            func.min(Employee.salary).label("global_min"),
            func.max(Employee.salary).label("global_max"),
            func.avg(Employee.salary).label("global_avg"),
        )
        .filter(Employee.is_active == True)
        .first()
    )

    countries = (
        db.query(Employee.country, func.count(Employee.id).label("count"))
        .filter(Employee.is_active == True)
        .group_by(Employee.country)
        .order_by(func.count(Employee.id).desc())
        .limit(10)
        .all()
    )

    departments = (
        db.query(Employee.department, func.avg(Employee.salary).label("avg"))
        .filter(Employee.is_active == True, Employee.department.isnot(None))
        .group_by(Employee.department)
        .order_by(func.avg(Employee.salary).desc())
        .all()
    )

    return {
        "total_employees": result.total_employees,
        "global_min_salary": result.global_min,
        "global_max_salary": result.global_max,
        "global_avg_salary": round(result.global_avg, 2),
        "top_countries_by_headcount": [
            {"country": c.country, "headcount": c.count}
            for c in countries
        ],
        "avg_salary_by_department": [
            {"department": d.department, "avg_salary": round(d.avg, 2)}
            for d in departments
        ],
    }