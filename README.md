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

# Seed 10,000 employees
python scripts/seed.py

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