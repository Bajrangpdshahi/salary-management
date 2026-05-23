.PHONY: test run seed lint

test:
	pytest tests/ -v --cov=app --cov-report=term-missing

run:
	uvicorn app.main:app --reload --port 8000

seed:
	python scripts/seed.py

lint:
	ruff check app/ tests/
	mypy app/