# Architecture Decisions

## 1. SQLite vs PostgreSQL

**Chosen: SQLite**

- The assessment specification requires SQLite.
- Railway supports persistent volumes, so the SQLite file survives redeploys.
- SQLAlchemy abstracts the database layer — swapping to PostgreSQL is a one-line change in `DATABASE_URL`.
- SQLite WAL mode provides adequate concurrency for HR tool read patterns.
- For writes, SQLite serializes; acceptable for a single-organization HR tool.

## 2. Server-Side Pagination vs Client-Side Filtering

**Chosen: Server-side pagination for everything**

- The UI sends `limit`, `offset`, `search`, and `country` parameters to the API.
- 10,000 employee records would degrade browser performance if loaded at once.
- Every search keystroke triggers an API call (debounced to 300ms) — this is the standard production pattern.
- The API returns `PaginatedEmployees` with `total`, `limit`, `offset`, and `data[]`.

## 3. Soft Delete vs Hard Delete

**Chosen: Soft delete (`is_active=False`)**

- HR data requires audit history for compliance.
- Accidental deletes should be recoverable.
- Implementation: `Employee.is_active` boolean field with `default=True`.
- All repository queries filter `WHERE is_active = TRUE` by default.
- The DELETE endpoint sets `is_active=False` rather than removing the row.

## 4. ORM vs Raw SQL for CRUD vs Seeding

**Chosen: Hybrid approach**

- **CRUD operations**: SQLAlchemy ORM — it's clean, pythonic, and sufficient for single-record operations.
- **Insights queries**: ORM with aggregate functions (`func.min`, `func.max`, `func.avg`) — readable and well-tested.
- **Seed script**: SQLAlchemy Core with `executemany()` — bypasses ORM overhead for 10,000-row bulk insert.
  - ORM-based seeding: ~15 seconds
  - Core-based seeding: ~2 seconds (7.5x faster)
- The trade-off is slightly less pythonic seeder code for a significant performance gain.

## 5. Percentile Calculation: Python vs SQL

**Chosen: Python in-memory computation**

- Load all salaries for a country (~10,000 max), sort, and compute percentiles in Python.
- Uses linear interpolation for accurate percentile calculation.
- For 10,000 floats: <10ms execution time.
- SQL alternative (window functions like `NTILE`, `PERCENT_RANK`) is more complex to write, test, and maintain.
- **If scale grows**: Switch to SQL window functions when datasets exceed 100,000 rows.

## 6. Layer Architecture: Repository → Service → Router

```
Router (HTTP concerns: status codes, path params, query params)
  ↓ calls
Service (Business logic: validation rules, domain constraints)
  ↓ calls
Repository (Data access: SQLAlchemy queries, pagination, filters)
  ↓ uses
Model (SQLAlchemy ORM: table definition, constraints, indexes)
```

**Rationale:**
- **Repository** isolates data access — if we switch databases, only this layer changes.
- **Service** enforces business rules — validation lives here, not in HTTP handlers.
- **Router** handles HTTP concerns only — status codes, path parameters, response formatting.
- This separation enables testing each layer independently with appropriate test doubles.

## 7. In-Memory SQLite Testing with StaticPool

Tests use `sqlite:///:memory:` with `StaticPool` to ensure thread-safe database sharing between pytest fixtures and FastAPI's `TestClient`.

**Problem**: FastAPI's `TestClient` runs request handlers in separate anyio worker threads. SQLite's default in-memory databases are per-thread, causing "no such table" errors.

**Solution**: `StaticPool` ensures all threads share the same in-memory database connection.

```python
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # ← Critical for TestClient
)
```

## 8. Frontend Component Architecture

```
Providers (TanStack Query)
├── Layout (Navbar: Home | Employees | Insights)
│
├── / (Home)
│   └── Landing page with CTA buttons
│
├── /employees
│   ├── EmployeeSearch (300ms debounced input + country filter)
│   ├── EmployeeTable (paginated, sortable, edit/delete actions)
│   ├── EmployeeForm (Dialog: create/edit with validation)
│   └── DeleteConfirmDialog (Dialog: confirm before delete)
│
└── /insights
    ├── Global Summary Cards (total employees, global min/max/avg)
    ├── Country Selector → SalaryStatsCards + PercentileTable
    ├── Job Title Selector → JobTitleStatsCard
    └── Bar Charts (top countries by headcount, avg salary by department)
```

## 9. Database Indexes

| Index | Columns | Purpose |
|-------|---------|---------|
| `idx_employees_country_active` | `(country, is_active)` | Every insight query filters on both |
| `idx_employees_jobtitle_country` | `(job_title, country, is_active)` | `GET /insights/job-title` endpoint |
| `idx_employees_fullname` | `(full_name)` | Search bar ILIKE queries |

## 10. Performance Characteristics

| Operation | Strategy | Expected |
|-----------|----------|----------|
| Seed 10,000 employees | Batched Core inserts, WAL mode | < 3 seconds |
| List employees (paginated) | Index on is_active + limit/offset | < 50ms |
| Search by name | ILIKE with index | < 100ms |
| Country salary stats | Composite index (country, is_active) | < 50ms |
| Job title stats | Composite index (job_title, country, is_active) | < 50ms |