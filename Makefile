PORT ?= 8001

dev:
	poetry run uvicorn referral_system.main:app --reload --port $(PORT)

firstmig:
	poetry run alembic revision -m "init_migration" --autogenerate

migrate:
	poetry run alembic upgrade head

install:
	poetry install

lint:
	poetry run ruff check

deploy:
	poetry run alembic revision -m "init_migration" --autogenerate
	alembic upgrade head
	poetry run uvicorn referral_system.main:app --port $(PORT)