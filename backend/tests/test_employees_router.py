"""
[TDD-RED] HTTP-level test suite for /api/employees endpoints.

Tests use FastAPI TestClient with in-memory SQLite (conftest.py fixture).
Each test exercises the full stack: router → service → repository → DB.
"""


class TestEmployeesRouter:

    def test_create_employee_returns_201(self, client):
        """POST /api/employees with valid data returns 201 + the created employee."""
        response = client.post(
            "/api/employees",
            json={
                "full_name": "Alice Smith",
                "job_title": "Senior Engineer",
                "country": "India",
                "salary": 120000,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["full_name"] == "Alice Smith"

    def test_create_employee_with_negative_salary_returns_422(self, client):
        """Pydantic validation (ge=0) rejects negative salary at the schema level."""
        response = client.post(
            "/api/employees",
            json={
                "full_name": "Bob",
                "job_title": "Analyst",
                "country": "USA",
                "salary": -500,
            },
        )
        assert response.status_code == 422

    def test_get_employee_not_found_returns_404(self, client):
        """GET /api/employees/{id} for a non-existent ID returns 404."""
        response = client.get("/api/employees/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_list_employees_returns_paginated(self, client):
        """GET /api/employees returns a paginated list with total count."""
        for i in range(5):
            client.post(
                "/api/employees",
                json={
                    "full_name": f"Employee {i}",
                    "job_title": "Dev",
                    "country": "India",
                    "salary": 60000,
                },
            )
        response = client.get("/api/employees?limit=3&offset=0")
        assert response.status_code == 200
        body = response.json()
        assert len(body["data"]) == 3
        assert body["total"] == 5

    def test_update_employee_returns_updated_data(self, client):
        """PUT /api/employees/{id} updates fields and returns the updated record."""
        created = client.post(
            "/api/employees",
            json={
                "full_name": "Old Name",
                "job_title": "Dev",
                "country": "India",
                "salary": 60000,
            },
        ).json()
        response = client.put(
            f"/api/employees/{created['id']}", json={"salary": 75000}
        )
        assert response.status_code == 200
        assert response.json()["salary"] == 75000

    def test_delete_employee_returns_204(self, client):
        """DELETE /api/employees/{id} soft-deletes and returns 204; subsequent GET returns 404."""
        created = client.post(
            "/api/employees",
            json={
                "full_name": "To Delete",
                "job_title": "Dev",
                "country": "India",
                "salary": 60000,
            },
        ).json()
        response = client.delete(f"/api/employees/{created['id']}")
        assert response.status_code == 204
        # Verify soft-delete — employee is now excluded from active listing
        get_response = client.get(f"/api/employees/{created['id']}")
        assert get_response.status_code == 404