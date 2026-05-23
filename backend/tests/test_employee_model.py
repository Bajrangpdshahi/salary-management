"""
[TDD-RED] Test suite for Employee SQLAlchemy model.

These tests verify:
1. Required fields (full_name, job_title, country, salary) cause DB errors if missing
2. Default values are applied correctly
3. Optional fields can be set
4. __repr__ returns expected format
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base


@pytest.fixture(scope="function")
def engine():
    """Creates a fresh in-memory SQLite database for model tests."""
    _engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(_engine)
    yield _engine
    Base.metadata.drop_all(_engine)


@pytest.fixture(scope="function")
def session(engine):
    """Creates a new session per test."""
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


class TestEmployeeModel:

    def test_employee_requires_full_name(self, session):
        """RED: Employee model must reject missing full_name at DB level."""
        from app.models.employee import Employee

        employee = Employee(
            job_title="Engineer",
            country="India",
            salary=100000,
        )
        session.add(employee)
        with pytest.raises(Exception):
            session.commit()

    def test_employee_requires_job_title(self, session):
        """RED: Employee model must reject missing job_title."""
        from app.models.employee import Employee

        employee = Employee(
            full_name="Alice Smith",
            country="India",
            salary=100000,
        )
        session.add(employee)
        with pytest.raises(Exception):
            session.commit()

    def test_employee_requires_country(self, session):
        """RED: Employee model must reject missing country."""
        from app.models.employee import Employee

        employee = Employee(
            full_name="Alice Smith",
            job_title="Engineer",
            salary=100000,
        )
        session.add(employee)
        with pytest.raises(Exception):
            session.commit()

    def test_employee_requires_salary(self, session):
        """RED: Employee model must reject missing salary."""
        from app.models.employee import Employee

        employee = Employee(
            full_name="Alice Smith",
            job_title="Engineer",
            country="India",
        )
        session.add(employee)
        with pytest.raises(Exception):
            session.commit()

    def test_employee_created_with_valid_data(self, session):
        """Employee can be created with all required + optional fields."""
        from app.models.employee import Employee
        from datetime import date

        employee = Employee(
            full_name="Alice Smith",
            job_title="Senior Engineer",
            department="Engineering",
            country="India",
            salary=120000.00,
            currency="USD",
            employment_type="Full-time",
            hire_date=date(2020, 1, 15),
            is_active=True,
        )
        session.add(employee)
        session.commit()

        assert employee.id is not None
        assert employee.full_name == "Alice Smith"
        assert employee.job_title == "Senior Engineer"
        assert employee.department == "Engineering"
        assert employee.country == "India"
        assert employee.salary == 120000.00
        assert employee.currency == "USD"
        assert employee.employment_type == "Full-time"
        assert employee.hire_date == date(2020, 1, 15)
        assert employee.is_active is True
        assert employee.created_at is not None

    def test_employee_default_values(self, session):
        """Employee defaults: currency='USD', employment_type='Full-time', is_active=True."""
        from app.models.employee import Employee

        employee = Employee(
            full_name="Bob Jones",
            job_title="Developer",
            country="UK",
            salary=75000,
        )
        session.add(employee)
        session.commit()

        assert employee.currency == "USD"
        assert employee.employment_type == "Full-time"
        assert employee.is_active is True

    def test_employee_repr(self, session):
        """__repr__ returns a meaningful string."""
        from app.models.employee import Employee

        employee = Employee(
            full_name="Charlie",
            job_title="Manager",
            country="USA",
            salary=95000,
        )
        session.add(employee)
        session.commit()

        repr_str = repr(employee)
        assert "Charlie" in repr_str
        assert "Manager" in repr_str
        assert str(employee.id) in repr_str

    def test_employee_optional_fields_are_nullable(self, session):
        """Optional fields (department, hire_date) can be None."""
        from app.models.employee import Employee

        employee = Employee(
            full_name="Diana",
            job_title="Analyst",
            country="UK",
            salary=65000,
            department=None,
            hire_date=None,
        )
        session.add(employee)
        session.commit()

        assert employee.department is None
        assert employee.hire_date is None