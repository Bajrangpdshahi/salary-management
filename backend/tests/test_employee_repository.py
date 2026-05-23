"""
[TDD-RED] Test suite for EmployeeRepository.

Tests cover:
- add() persists and returns an employee with an ID
- get_by_id() returns None for missing
- list() supports pagination with limit/offset
- list() search filters by name (case-insensitive)
- list() search filters by job title
- list() excludes inactive employees
- soft_delete() sets is_active=False
- update() changes only specified fields
- count() returns correct totals
"""

import pytest
from app.repositories.employee_repository import EmployeeRepository


class TestEmployeeRepository:

    def test_add_returns_employee_with_id(self, db_session):
        """Add persists an employee and returns it with a generated ID."""
        repo = EmployeeRepository(db_session)
        employee = repo.add(
            full_name="Alice Smith",
            job_title="Engineer",
            country="India",
            salary=80000,
        )
        assert employee.id is not None
        assert employee.full_name == "Alice Smith"

    def test_get_by_id_returns_none_for_missing(self, db_session):
        """get_by_id returns None when no employee matches."""
        repo = EmployeeRepository(db_session)
        result = repo.get_by_id(9999)
        assert result is None

    def test_get_by_id_returns_correct_employee(self, db_session):
        """get_by_id returns the correct employee when found."""
        repo = EmployeeRepository(db_session)
        created = repo.add(
            full_name="Bob Jones",
            job_title="Manager",
            country="USA",
            salary=90000,
        )
        found = repo.get_by_id(created.id)
        assert found is not None
        assert found.full_name == "Bob Jones"
        assert found.salary == 90000

    def test_list_returns_paginated_results(self, db_session):
        """list() correctly paginates with limit and offset."""
        repo = EmployeeRepository(db_session)
        for i in range(25):
            repo.add(
                full_name=f"Employee {i}",
                job_title="Analyst",
                country="USA",
                salary=70000,
            )
        page1 = repo.list(limit=10, offset=0)
        page2 = repo.list(limit=10, offset=10)
        page3 = repo.list(limit=10, offset=20)
        assert len(page1) == 10
        assert len(page2) == 10
        assert len(page3) == 5

    def test_search_filters_by_name(self, db_session):
        """search parameter filters employees by full_name (case-insensitive)."""
        repo = EmployeeRepository(db_session)
        repo.add(full_name="John Doe", job_title="Manager", country="UK", salary=90000)
        repo.add(full_name="Jane Roe", job_title="Analyst", country="UK", salary=60000)
        results = repo.list(search="john", limit=10, offset=0)
        assert len(results) == 1
        assert results[0].full_name == "John Doe"

    def test_search_filters_by_job_title(self, db_session):
        """search parameter filters employees by job_title (case-insensitive)."""
        repo = EmployeeRepository(db_session)
        repo.add(full_name="Alice", job_title="Engineer", country="India", salary=80000)
        repo.add(full_name="Bob", job_title="Engineer", country="India", salary=85000)
        repo.add(full_name="Carol", job_title="Manager", country="India", salary=95000)
        results = repo.list(search="engineer", limit=10, offset=0)
        assert len(results) == 2

    def test_list_filters_by_country(self, db_session):
        """list() supports country filter."""
        repo = EmployeeRepository(db_session)
        repo.add(full_name="A", job_title="Dev", country="India", salary=60000)
        repo.add(full_name="B", job_title="Dev", country="USA", salary=70000)
        repo.add(full_name="C", job_title="Dev", country="India", salary=80000)
        results = repo.list(country="India", limit=10, offset=0)
        assert len(results) == 2
        assert all(e.country == "India" for e in results)

    def test_list_excludes_inactive_employees_by_default(self, db_session):
        """list() should not return soft-deleted employees."""
        repo = EmployeeRepository(db_session)
        emp = repo.add(full_name="Deleted", job_title="Dev", country="India", salary=75000)
        repo.soft_delete(emp.id)
        results = repo.list(limit=10, offset=0)
        assert all(e.full_name != "Deleted" for e in results)

    def test_soft_delete_sets_is_active_false(self, db_session):
        """soft_delete marks the employee as inactive."""
        repo = EmployeeRepository(db_session)
        emp = repo.add(full_name="Bob", job_title="Dev", country="India", salary=75000)
        result = repo.soft_delete(emp.id)
        assert result is True
        found = repo.get_by_id(emp.id)
        assert found.is_active is False

    def test_soft_delete_nonexistent_returns_false(self, db_session):
        """soft_delete on non-existent ID returns False."""
        repo = EmployeeRepository(db_session)
        result = repo.soft_delete(99999)
        assert result is False

    def test_update_changes_specified_fields(self, db_session):
        """update() only modifies the fields passed."""
        repo = EmployeeRepository(db_session)
        emp = repo.add(full_name="Original", job_title="Dev", country="India", salary=60000)
        updated = repo.update(emp.id, salary=75000, department="Engineering")
        assert updated is not None
        assert updated.salary == 75000
        assert updated.department == "Engineering"
        assert updated.full_name == "Original"  # unchanged

    def test_update_nonexistent_returns_none(self, db_session):
        """update() on non-existent ID returns None."""
        repo = EmployeeRepository(db_session)
        result = repo.update(99999, salary=50000)
        assert result is None

    def test_count_returns_total_active(self, db_session):
        """count() returns correct number of active employees."""
        repo = EmployeeRepository(db_session)
        for i in range(15):
            repo.add(full_name=f"Emp {i}", job_title="Analyst", country="USA", salary=70000)
        total = repo.count()
        assert total == 15

    def test_count_with_search_filter(self, db_session):
        """count() respects search filter."""
        repo = EmployeeRepository(db_session)
        repo.add(full_name="John", job_title="Engineer", country="India", salary=80000)
        repo.add(full_name="Jane", job_title="Analyst", country="India", salary=60000)
        total = repo.count(search="john")
        assert total == 1