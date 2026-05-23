"""
Employee SQLAlchemy ORM model for the Salary Management Tool.

Represents a single employee record with all fields as designed
in the database schema (INCUBYTE_ASSESSMENT_PLAN.md Section 8).
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False, index=True)
    job_title = Column(String(255), nullable=False, index=True)
    department = Column(String(255), nullable=True)
    country = Column(String(100), nullable=False, index=True)
    salary = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    employment_type = Column(String(50), nullable=False, default="Full-time")
    hire_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Employee {self.id}: {self.full_name} ({self.job_title})>"