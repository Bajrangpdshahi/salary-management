"""
[TDD-RED] Test suite for EmployeeService — business logic layer.

Tests cover:
- Negative salary raises ValueError
- Empty/whitespace full_name raises ValueError
- Empty job_title raises ValueError
- Empty country raises ValueError
- Valid data creates an employee through the repository
"""

import pytest
from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService


class TestEmployeeService:

    def test_add_employee_raises_on_negative_salary(self, db_session):
        """Negative salary must be rejected at the service layer."""
        service = EmployeeService(EmployeeRepository(db_session))
        with pytest.raises(ValueError, match="Salary must be non-negative"):
            service.add_employee(
                full_name="Alice",
                job_title="Eng",
                country="India",
                salary=-1000,
            )

    def test_add_employee_raises_on_empty_name(self, db_session):
        """Empty or whitespace-only full_name must be rejected."""
        service = EmployeeService(EmployeeRepository(db_session))
        with pytest.raises(ValueError, match="Full name cannot be empty"):
            service.add_employee(
                full_name="   ",
                job_title="Eng",
                country="India",
                salary=50000,
            )

    def test_add_employee_raises_on_empty_job_title(self, db_session):
        """Empty job_title must be rejected."""
        service = EmployeeService(EmployeeRepository(db_session))
        with pytest.raises(ValueError, match="Job title cannot be empty"):
            service.add_employee(
                full_name="Alice",
                job_title="",
                country="India",
                salary=50000,
            )

    def test_add_employee_raises_on_empty_country(self, db_session):
        """Empty country must be rejected."""
        service = EmployeeService(EmployeeRepository(db_session))
        with pytest.raises(ValueError, match="Country cannot be empty"):
            service.add_employee(
                full_name="Alice",
                job_title="Eng",
                country="",
                salary=50000,
            )

    def test_add_employee_returns_created_employee(self, db_session):
        """Valid employee data should flow through to the repository and
        return a persisted employee with a generated ID."""
        service = EmployeeService(EmployeeRepository(db_session))
        emp = service.add_employee(
            full_name="Alice Smith",
            job_title="Senior Engineer",
            country="India",
            salary=120000,
        )
        assert emp.id is not None
        assert emp.full_name == "Alice Smith"
        assert emp.salary == 120000