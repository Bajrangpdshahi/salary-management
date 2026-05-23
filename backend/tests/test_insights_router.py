"""Phase 5 — Salary Insights Router Tests (TDD-RED)

Tests for:
  - GET /api/insights/country/{country} — min/max/avg/median/percentiles/headcount
  - GET /api/insights/job-title?country=X&job_title=Y — filtered stats
  - GET /api/insights/summary — global org-wide summary
"""


class TestInsightsRouter:
    """Salary insights & analytics endpoint tests."""

    def _seed_employees(self, client, employees: list[dict]):
        """Helper to seed employees via the existing POST /api/employees endpoint."""
        for emp in employees:
            client.post("/api/employees", json=emp)

    # ------------------------------------------------------------------
    # Country stats
    # ------------------------------------------------------------------
    def test_country_stats_returns_min_max_avg(self, client):
        """Assert country-level stats: min, max, avg, median, headcount."""
        self._seed_employees(client, [
            {"full_name": "A", "job_title": "Dev", "country": "India", "salary": 60000},
            {"full_name": "B", "job_title": "Mgr", "country": "India", "salary": 90000},
            {"full_name": "C", "job_title": "Dev", "country": "India", "salary": 75000},
            {"full_name": "D", "job_title": "Dev", "country": "USA", "salary": 120000},
        ])

        response = client.get("/api/insights/country/India")
        assert response.status_code == 200

        data = response.json()
        assert data["min_salary"] == 60000
        assert data["max_salary"] == 90000
        assert data["avg_salary"] == 75000
        assert data["median_salary"] == 75000
        assert data["headcount"] == 3

    # ------------------------------------------------------------------
    # Job-title stats
    # ------------------------------------------------------------------
    def test_job_title_stats_filters_by_country_and_title(self, client):
        """Assert job-title stats filtered by country and title."""
        self._seed_employees(client, [
            {"full_name": "A", "job_title": "Engineer", "country": "India", "salary": 80000},
            {"full_name": "B", "job_title": "Engineer", "country": "India", "salary": 100000},
            {"full_name": "C", "job_title": "Manager", "country": "India", "salary": 120000},
        ])

        response = client.get(
            "/api/insights/job-title?country=India&job_title=Engineer"
        )
        assert response.status_code == 200

        data = response.json()
        assert data["avg_salary"] == 90000
        assert data["headcount"] == 2

    # ------------------------------------------------------------------
    # 404 for unknown country
    # ------------------------------------------------------------------
    def test_country_stats_returns_404_for_unknown_country(self, client):
        """Assert 404 when no employees exist in the given country."""
        response = client.get("/api/insights/country/Narnia")
        assert response.status_code == 404

    # ------------------------------------------------------------------
    # Percentiles
    # ------------------------------------------------------------------
    def test_percentiles_are_returned(self, client):
        """Assert p25/p50/p75/p90 percentile keys are present."""
        salaries = [50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000]
        for i, sal in enumerate(salaries):
            client.post("/api/employees", json={
                "full_name": f"Emp {i}",
                "job_title": "Dev",
                "country": "India",
                "salary": sal,
            })

        response = client.get("/api/insights/country/India")
        data = response.json()

        assert "p25" in data
        assert "p50" in data
        assert "p75" in data
        assert "p90" in data