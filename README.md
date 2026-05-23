# Salary Management Tool

**Incubyte Assessment — Software Craftsperson/Python-AI-III**

A full-stack salary management application built with strict TDD discipline, designed for HR managers to manage 10,000+ employee records with search, pagination, and salary analytics.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12+, FastAPI, SQLAlchemy ORM + Core, SQLite |
| Frontend | Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui |
| State | TanStack Query (React Query) |
| Charts | Recharts |
| Testing | pytest (37 tests, 100% pass), coverage ≥ 90% |
| CI/CD | GitHub Actions |

## Project Structure

```
salary-management/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app factory + CORS
│   │   ├── database.py          # SQLAlchemy engine + session
│   │   ├── models/employee.py   # Employee ORM model
│   │   ├── schemas/employee.py  # Pydantic request/response schemas
│   │   ├── repositories/        # Data access layer
│   │   ├── services/            # Business logic + validation
│   │   └── routers/             # API endpoints (CRUD + insights)
│   ├── tests/                   # 37 tests: model, repo, service, router
│   ├── scripts/seed.py          # 10k employee bulk seeder
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js App Router pages
│   │   ├── components/
│   │   │   ├── ui/              # shadcn/ui components (8 components)
│   │   │   ├── employees/       # EmployeeTable, Form, Search, DeleteDialog
│   │   │   └── insights/        # Dashboard, StatsCard, PercentileTable, BarChart
│   │   ├── lib/                 # API client, hooks, utils
│   │   └── types/               # TypeScript interfaces
│   └── package.json
├── .github/workflows/ci.yml     # Backend tests + Frontend build
└── docs/
    ├── architecture.md           # Architecture decisions
    └── ai-prompts.md             # AI prompt transcripts
```

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+
- npm 11+

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Seed 10,000 employees (idempotent — safe to rerun)
python scripts/seed.py

# Re-seed from scratch (delete old DB first)
del app\salary_management.db && python scripts/seed.py   # Windows
rm app/salary_management.db && python scripts/seed.py    # macOS/Linux

# Or via Make:
make seed

# Start the API server
uvicorn app.main:app --reload
```

API docs available at http://localhost:8000/docs

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend at http://localhost:3000

## API Endpoints

### Employees
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/employees` | Create employee |
| `GET` | `/api/employees` | List (paginated, searchable, filterable) |
| `GET` | `/api/employees/{id}` | Get by ID |
| `PUT` | `/api/employees/{id}` | Update employee |
| `DELETE` | `/api/employees/{id}` | Soft delete |

**Query params for GET /api/employees:**
- `limit` (int, default=50, max=500)
- `offset` (int, default=0)
- `search` (string, ILIKE on name & job title)
- `country` (string, exact match)

### Insights
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/insights/country/{country}` | Country salary stats + percentiles |
| `GET` | `/api/insights/job-title?country=&job_title=` | Job title stats in country |
| `GET` | `/api/insights/summary` | Global org summary |

### Meta
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Swagger UI |

## Seeding — 10,000 Employee Data Generator

The seed script populates the database with realistic synthetic employee records for development and testing.

### Quick Run (from `backend/` directory)

```bash
# Method 1: Direct Python (recommended for CI/CD)
python scripts/seed.py

# Method 2: Via Make
make seed
```

### Command-Line Options

| Flag | Shorthand | Default | Description |
|------|-----------|---------|-------------|
| `--count` | `-c` | `10000` | Number of employees to generate |

```bash
# Seed exactly 10,000 (default)
python scripts/seed.py

# Seed 5,000 employees
python scripts/seed.py --count 5000
python scripts/seed.py -c 5000

# Seed 50,000 employees (for load testing)
python scripts/seed.py --count 50000
```

### Data Generation Strategy

| Attribute | Source | Details |
|-----------|--------|---------|
| **Full Name** | `first_names.txt` (140 names) × `last_names.txt` (150 names) | 21,000 unique combinations, chosen randomly |
| **Job Title** | 16 predefined titles | Software Engineer → Sales Executive |
| **Salary** | Per-title salary bands | e.g., Software Engineer: $60K–$100K; Principal Engineer: $160K–$220K |
| **Department** | 9 departments | Engineering, Product, Data, Operations, Marketing, Sales, HR, Finance, Design |
| **Country** | 10 countries | India, USA, UK, Germany, Canada, Australia, Singapore, Brazil, France, Japan |
| **Currency** | Hardcoded `USD` | All salaries in USD for consistent comparison |
| **Employment Type** | Weighted random | 75% Full-time, 25% Contractor |
| **Hire Date** | Random within 10 years | `today - 30–3650 days` |

### Performance

| Records | Batch Size | Journal Mode | Sync | Expected Time | Throughput |
|---------|------------|-------------|------|--------------|------------|
| 10,000 | 1,000 | WAL | NORMAL | < 3 seconds | ~5,000 rows/sec |
| 50,000 | 1,000 | WAL | NORMAL | ~10–15 seconds | ~3,500 rows/sec |

**Performance strategy:**
- Uses **SQLAlchemy Core** `executemany()` (not ORM) — bypasses object-mapping overhead
- Enables **SQLite WAL mode** for concurrent reads during writes
- Sets **synchronous=NORMAL** (not FULL) for faster writes with acceptable crash safety
- Batches inserts at **1,000 rows per transaction** to balance memory and commit frequency

### Idempotency

The script is **safe to run repeatedly**. It checks the current employee count before inserting:

| Condition | Behavior |
|-----------|----------|
| Current count < target count | Inserts `target - current` additional rows |
| Current count >= target count | Skips (no duplicates, no changes) |

This means if you already have 103 employees and run `--count 5`, you'll see:

```
Already have 103 employees (target: 5). Skipping seed.
```

**This is not an error** — it means the DB already has more employees than requested. To re-seed with a fresh set, delete the DB first (see "Resetting" below).

```bash
# Run it 3 times — same result, no duplicates
$ python scripts/seed.py
[OK] Seeded 10000 employees in 2.34s (4274 records/sec)

$ python scripts/seed.py
Already have 10000 employees (target: 10000). Skipping seed.

$ python scripts/seed.py -c 5000
Already have 10000 employees (target: 5000). Skipping seed.
```

### Resetting the Database

To wipe all data and start fresh:

```bash
# Delete the database file
del app\salary_management.db       # Windows
rm app/salary_management.db        # macOS/Linux

# Re-seed
python scripts/seed.py
```

### Verification

After seeding, verify via API:

```bash
curl http://localhost:8000/api/employees?limit=5
curl http://localhost:8000/api/insights/summary
```

Or check the database directly:

```bash
python -c "import sqlite3; c=sqlite3.connect('app/salary_management.db'); print(c.execute('SELECT COUNT(*) FROM employees').fetchone()[0]); c.close()"
```

## Test Results

```
37 passed in 1.23s
Coverage: 92% (target: 90%)
```

| Test Suite | Tests | Status |
|-----------|-------|--------|
| test_employee_model | 8 | ✅ |
| test_employee_repository | 14 | ✅ |
| test_employee_service | 5 | ✅ |
| test_employees_router | 6 | ✅ |
| test_insights_router | 4 | ✅ |

## TDD Discipline

This project follows the Three Laws of TDD:
1. **RED** — Write a failing test first
2. **GREEN** — Write minimal code to pass
3. **REFACTOR** — Clean up without changing behavior

Every commit is tagged with `[TDD-RED]`, `[TDD-GREEN]`, or `[REFACTOR]`.

## Architecture Decisions

See [`docs/architecture.md`](docs/architecture.md) for:
- Why SQLite (not PostgreSQL)
- Why server-side pagination (not client-side)
- Why soft delete (not hard delete)
- Why ORM for CRUD + Core for seeding
- Why Python percentiles (not SQL window functions)

## AI Prompts

See [`docs/ai-prompts.md`](docs/ai-prompts.md) for the actual prompts used to guide AI-assisted development throughout this project.

## License

Built for Incubyte assessment submission.