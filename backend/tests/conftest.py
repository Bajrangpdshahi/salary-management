import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure all models are imported before any fixture creates tables
from app.database import Base, get_db
from app.models import employee  # noqa: F401 — registers Employee with Base.metadata

from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def db_session():
    """Creates a fresh in-memory SQLite database per test.

    Uses StaticPool so that the test thread and the FastAPI handler thread
    (via anyio/TestClient) share the **same** in-memory SQLite database.
    Without StaticPool, each thread gets its own isolated :memory: database.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI TestClient with overridden DB dependency."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)