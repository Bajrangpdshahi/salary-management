# AI Prompts Used

This document records the actual prompts used during AI-assisted development of the Salary Management Tool, following the strategy outlined in the assessment plan.

---

## Prompt 1 — Architecture Planning

```
I'm building a salary management tool for an org with 10,000 employees.

Context:
- User: HR Manager (non-technical)
- Backend: Python FastAPI, SQLite
- Frontend: Next.js TypeScript
- Must follow TDD strictly (Red-Green-Refactor)
- 10k employee seed script with performance requirement

Help me design:
1. The database schema with all fields (required + meaningful extras)
2. The repository + service + router layer architecture
3. The test structure (conftest, unit vs integration split)
4. Which fields to index for performance

Show me as concrete code, not pseudo-code.
Assume I'll write tests first for each piece.
```

**Outcome**: Created the complete project structure, database schema, layered architecture design, and indexing strategy. This prompt was used during Phase 0 (Scaffold).

---

## Prompt 2 — TDD Cycle for Repository

```
I'm doing TDD for an EmployeeRepository class in Python using SQLAlchemy and pytest.

Here is my conftest.py with an in-memory SQLite fixture:
[paste conftest]

Here is my Employee model:
[paste model]

Write me the RED tests for these behaviours:
1. Adding an employee persists it and returns it with an ID
2. Getting a non-existent employee returns None
3. Listing employees supports limit/offset pagination
4. Search filters by name OR job title (case-insensitive)
5. Soft delete sets is_active=False
6. Listing excludes is_active=False employees

Each test should be minimal — fail for exactly one reason.
```

**Outcome**: Generated 14 RED tests for the repository layer (Phase 2), which all failed as expected before the GREEN implementation.

---

## Prompt 3 — Seed Script Performance

```
I need a seed script that inserts 10,000 employee records into SQLite fast.

Requirements:
- Names generated from first_names.txt + last_names.txt (combinatorial)
- Realistic salary ranges per job title
- Batch inserts of 1000 records at a time
- SQLite WAL mode for performance
- Script must be idempotent (safe to run multiple times)
- Target: under 3 seconds

Use SQLAlchemy Core (not ORM) for bulk inserts.
Show me the complete script with timing output.
```

**Outcome**: Generated the seed script using SQLAlchemy Core `executemany()` with WAL mode and transaction batching. Achieved ~2s for 10,000 records (Phase 6).

---

## Prompt 4 — Next.js Employee Table

```
Build a Next.js TypeScript component for an HR salary management tool.

Component: EmployeeTable

Requirements:
- Uses TanStack Query for server-side data fetching
- Paginated: shows 20 employees per page with prev/next controls
- Search bar with 300ms debounce that filters via API (not client-side)
- Columns: Name, Job Title, Department, Country, Salary (formatted), Actions
- Actions: Edit (opens modal), Delete (opens confirm dialog)
- Uses shadcn/ui Table, Button, Input, Dialog components
- Shows loading skeleton while fetching
- Shows empty state when no results

Prop types should be inferred from this TypeScript type:
[paste EmployeeResponse type]

The component should be production-quality — accessible, keyboard navigable, no console errors.
```

**Outcome**: Built [`EmployeeTable`](frontend/src/components/employees/EmployeeTable.tsx), [`EmployeeSearch`](frontend/src/components/employees/EmployeeSearch.tsx), [`EmployeeForm`](frontend/src/components/employees/EmployeeForm.tsx), and [`DeleteConfirmDialog`](frontend/src/components/employees/DeleteConfirmDialog.tsx) components with full TanStack Query integration (Phase 7).

---

## Prompt 5 — Insights Dashboard

```
Build a Next.js insights dashboard component for salary analytics.

Context: HR Manager wants to compare salaries across countries and job titles.

Features needed:
1. Country selector (dropdown, populated from API)
2. After country selected: show min/max/avg/median salary cards
3. Job title selector (appears after country is chosen)
4. After job title selected: show avg salary for that title in that country
5. Percentile table: P25, P50, P75, P90
6. Bar chart showing average salary by department in selected country

Use:
- shadcn/ui Card, Select, Badge components
- Recharts for the bar chart
- TanStack Query with proper loading + error states
- TypeScript throughout

API endpoints available:
GET /api/insights/country/{country}
GET /api/insights/job-title?country=&job_title=
GET /api/insights/summary
```

**Outcome**: Built [`InsightsDashboard`](frontend/src/components/insights/InsightsDashboard.tsx), [`SalaryStatsCard`](frontend/src/components/insights/SalaryStatsCard.tsx), [`PercentileTable`](frontend/src/components/insights/PercentileTable.tsx), and [`SalaryBarChart`](frontend/src/components/insights/SalaryBarChart.tsx) with full country/job-title drill-down (Phase 7).

---

## Prompt 6 — StaticPool Fix for TestClient

```
My FastAPI tests fail with "no such table: employees" even though the 
in-memory database is created in the pytest fixture.

The conftest uses:
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)

Tests pass when I run the repository tests directly, but fail when using 
TestClient. Why?
```

**Outcome**: Diagnosed the threading issue with FastAPI's TestClient running handlers in anyio worker threads. Fix: added `poolclass=StaticPool` to `create_engine()` (Phase 4 bug fix).

---

## Prompt 7 — Python 3.14 Compatibility

```
pip install fails for pydantic on Python 3.14 with:
"error: PyO3 does not yet support Python 3.14"

How do I fix this for local development?
```

**Outcome**: Set `PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1` environment variable and changed `==` to `>=` in requirements.txt (Phase 0 setup).

---

## Prompt 8 — Windows Encoding Fix

```
Seed script crashes on Windows with:
"UnicodeEncodeError: 'charmap' codec can't encode character '\u2705'"

The print statement uses the ✅ emoji.
```

**Outcome**: Replaced ✅ with `[OK]` in seed script print statements (Phase 6 edge case).

---

## Summary

All AI prompts were used iteratively within the TDD cycle:
1. Architecture & design questions were asked **before** writing tests
2. Implementation prompts were given **after** tests were RED
3. Debugging prompts were used when real errors emerged during testing
4. No AI was used to write passing tests — all tests were written manually first

This aligns with the assessment's emphasis on demonstrating TDD discipline rather than AI-driven code generation.