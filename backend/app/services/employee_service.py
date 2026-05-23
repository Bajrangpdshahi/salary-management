"""
EmployeeService — business logic and validation layer.

Sits between the API routers and the repository layer.
Validates input data (salary, names, country) before delegating
to the pure data-access repository.
"""

from app.repositories.employee_repository import EmployeeRepository
from app.models.employee import Employee


class EmployeeService:
    def __init__(self, repository: EmployeeRepository):
        self.repo = repository

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    def _validate_employee_data(
        self,
        full_name: str,
        job_title: str,
        country: str,
        salary: float,
    ) -> None:
        """Raise ValueError if any required field fails validation."""
        if not full_name or not full_name.strip():
            raise ValueError("Full name cannot be empty")
        if not job_title or not job_title.strip():
            raise ValueError("Job title cannot be empty")
        if not country or not country.strip():
            raise ValueError("Country cannot be empty")
        if salary < 0:
            raise ValueError("Salary must be non-negative")

    # ------------------------------------------------------------------
    # Public API — mirrors the repository but adds validation
    # ------------------------------------------------------------------

    def add_employee(
        self,
        full_name: str,
        job_title: str,
        country: str,
        salary: float,
        **kwargs,
    ) -> Employee:
        """Validate and then persist a new employee."""
        self._validate_employee_data(full_name, job_title, country, salary)
        return self.repo.add(
            full_name=full_name.strip(),
            job_title=job_title.strip(),
            country=country.strip(),
            salary=salary,
            **kwargs,
        )

    def update_employee(self, employee_id: int, **kwargs) -> Employee | None:
        """Update an employee, validating salary if provided."""
        if "salary" in kwargs and kwargs["salary"] is not None:
            if kwargs["salary"] < 0:
                raise ValueError("Salary must be non-negative")
        return self.repo.update(employee_id, **kwargs)

    def delete_employee(self, employee_id: int) -> bool:
        """Soft-delete an employee (marks is_active=False)."""
        return self.repo.soft_delete(employee_id)

    def get_employee(self, employee_id: int) -> Employee | None:
        """Return a single employee by ID."""
        return self.repo.get_by_id(employee_id)

    def list_employees(
        self,
        limit: int = 50,
        offset: int = 0,
        search: str | None = None,
        country: str | None = None,
    ) -> dict:
        """Return a paginated dict with data, total, limit, offset."""
        employees = self.repo.list(
            limit=limit, offset=offset, search=search, country=country
        )
        total = self.repo.count(search=search, country=country)
        return {"data": employees, "total": total, "limit": limit, "offset": offset}