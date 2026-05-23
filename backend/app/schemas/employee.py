"""
Pydantic v2 schemas for Employee API request/response validation.

- EmployeeCreate: validates input on POST /api/employees
- EmployeeUpdate: partial update (all fields optional)
- EmployeeResponse: serializes SQLAlchemy model → JSON
- PaginatedEmployees: wraps list response with pagination metadata
"""

from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional


class EmployeeCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    job_title: str = Field(..., min_length=1, max_length=255)
    department: Optional[str] = None
    country: str = Field(..., min_length=1, max_length=100)
    salary: float = Field(..., ge=0)
    currency: str = Field(default="USD", max_length=10)
    employment_type: str = Field(default="Full-time")
    hire_date: Optional[date] = None

    @field_validator("full_name", "job_title", "country")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    country: Optional[str] = None
    salary: Optional[float] = Field(default=None, ge=0)
    currency: Optional[str] = None
    employment_type: Optional[str] = None
    hire_date: Optional[date] = None


class EmployeeResponse(BaseModel):
    id: int
    full_name: str
    job_title: str
    department: Optional[str]
    country: str
    salary: float
    currency: str
    employment_type: str
    hire_date: Optional[date]
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PaginatedEmployees(BaseModel):
    data: list[EmployeeResponse]
    total: int
    limit: int
    offset: int