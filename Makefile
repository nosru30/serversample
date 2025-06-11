# ----------------------------------------
# Common development commands
# ----------------------------------------

PYTHON ?= python
VENV_ACTIVATE = source .venv/bin/activate

# Default target
.DEFAULT_GOAL := help

# ---------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------
help:
	@echo "make setup         - Create venv & install deps (online first, cache wheels)"
	@echo "make migrate       - Run DB migration (uses DATABASE_URL or SQLite fallback)"
	@echo "make lint          - Run Ruff linter"
	@echo "make test          - Run Ruff + pytest"
	@echo "make start         - 🚀 Start full stack with Docker (recommended)"
	@echo "make start-local   - Run FastAPI locally with uvicorn (reload, no Docker)"
	@echo "make compose-up    - Start docker-compose (detached)"
	@echo "make compose-down  - Stop docker-compose"

# ---------------------------------------------------------------------
# Main tasks
# ---------------------------------------------------------------------
setup:
	./setup_env.sh

migrate:
	$(VENV_ACTIVATE) && $(PYTHON) -m app.migrate

test: lint
	$(VENV_ACTIVATE) && pytest

lint:
	$(VENV_ACTIVATE) && ruff check .

start:
	docker-compose up --build

start-local:
	$(VENV_ACTIVATE) && uvicorn app.main:app --reload

compose-up:
	docker-compose up -d

compose-down:
	docker-compose down
