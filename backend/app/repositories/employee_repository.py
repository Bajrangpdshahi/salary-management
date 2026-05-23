"""
EmployeeRepository — pure data-access layer for Employee entities.

All methods accept a SQLAlchemy Session and perform no business logic.
This keeps the repository testable with an in-memory SQLite database.
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.employee import Employee


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, **kwargs) -> Employee:
        """Persist a new employee and return it with the generated ID."""
        employee = Employee(**kwargs)
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def get_by_id(self, employee_id: int) -> Employee | None:
        """Return the employee with the given ID, or None if not found."""
        return self.db.query(Employee).filter(Employee.id == employee_id).first()

    def list(
        self,
        limit: int = 50,
        offset: int = 0,
        search: str | None = None,
        country: str | None = None,
    ) -> list[Employee]:
        """Return a paginated list of active employees, optionally filtered."""
        query = self.db.query(Employee).filter(Employee.is_active == True)

        if search:
            query = query.filter(
                or_(
                    Employee.full_name.ilike(f"%{search}%"),
                    Employee.job_title.ilike(f"%{search}%"),
                )
            )
        if country:
            query = query.filter(Employee.country == country)

        return query.offset(offset).limit(limit).all()

    def count(
        self,
        search: str | None = None,
        country: str | None = None,
    ) -> int:
        """Return the total count of active employees with optional filters."""
        query = self.db.query(Employee).filter(Employee.is_active == True)

        if search:
            query = query.filter(
                or_(
                    Employee.full_name.ilike(f"%{search}%"),
                    Employee.job_title.ilike(f"%{search}%"),
                )
            )
        if country:
            query = query.filter(Employee.country == country)

        return query.count()

    def update(self, employee_id: int, **kwargs) -> Employee | None:
        """Update specific fields of an employee. Returns the updated employee or None."""
        employee = self.get_by_id(employee_id)
        if not employee:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(employee, key, value)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def soft_delete(self, employee_id: int) -> bool:
        """Mark an employee as inactive (soft delete). Returns True if found."""
        employee = self.get_by_id(employee_id)
        if not employee:
            return False
        employee.is_active = False
        self.db.commit()
        return True