"""
Routers for /api/employees — CRUD endpoints.

Each endpoint delegates to EmployeeService for business logic
and uses Pydantic schemas for request/response validation.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    PaginatedEmployees,
)

router = APIRouter(prefix="/api/employees", tags=["employees"])


def get_service(db: Session = Depends(get_db)) -> EmployeeService:
    """FastAPI dependency that builds the full service stack."""
    return EmployeeService(EmployeeRepository(db))


@router.post("", response_model=EmployeeResponse, status_code=201)
def create_employee(
    payload: EmployeeCreate,
    service: EmployeeService = Depends(get_service),
):
    """Create a new employee. Returns 201 on success, 422 on validation failure."""
    try:
        return service.add_employee(**payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("", response_model=PaginatedEmployees)
def list_employees(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    search: str | None = Query(None),
    country: str | None = Query(None),
    service: EmployeeService = Depends(get_service),
):
    """List active employees with pagination, optional search & country filter."""
    return service.list_employees(
        limit=limit, offset=offset, search=search, country=country
    )


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_service),
):
    """Retrieve a single employee by ID. Returns 404 if not found or inactive."""
    employee = service.get_employee(employee_id)
    if not employee or not employee.is_active:
        raise HTTPException(
            status_code=404, detail=f"Employee {employee_id} not found"
        )
    return employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
    service: EmployeeService = Depends(get_service),
):
    """Update an employee. Only supplied fields are changed. Returns 404 if missing."""
    try:
        updated = service.update_employee(
            employee_id,
            **{k: v for k, v in payload.model_dump().items() if v is not None},
        )
        if not updated:
            raise HTTPException(
                status_code=404, detail=f"Employee {employee_id} not found"
            )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/{employee_id}", status_code=204)
def delete_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_service),
):
    """Soft-delete an employee. Returns 204 on success, 404 if not found."""
    deleted = service.delete_employee(employee_id)
    if not deleted:
        raise HTTPException(
            status_code=404, detail=f"Employee {employee_id} not found"
        )