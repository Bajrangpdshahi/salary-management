from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

# Import models so they are registered with Base metadata
from app.models import employee  # noqa: F401

# Create all tables on startup (for development; use Alembic in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Salary Management Tool",
    description="Incubyte Assessment — Employee salary management API",
    version="1.0.0",
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
from app.routers import employees  # noqa: E402
from app.routers import insights  # noqa: E402

app.include_router(employees.router)
app.include_router(insights.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}