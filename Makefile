.PHONY: dev test lint type-check migrate

dev:
	docker compose up --build

down:
	docker compose down

test:
	pytest

lint:
	ruff check app tests
	ruff format --check app tests

format:
	ruff check --fix app tests
	ruff format app tests

type-check:
	mypy app

migrate:
	alembic upgrade head

migration:
	alembic revision --autogenerate -m "$(msg)"
