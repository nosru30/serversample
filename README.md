# serversample

## 🚀 Quickstart (Docker – recommended)

```bash
# Full stack (FastAPI + Postgres) will start on http://localhost:8000
make start
```

開発環境をシンプルに保ちたい場合は上記 `make start` だけで
コンテナが構築・起動します。停止は `make compose-down` です。

---

## Setup (using venv)

```bash
# Create virtual environment (Python 3.10 など)
python -m venv .venv

# Activate the environment
source .venv/bin/activate        # Linux/macOS
# .\\.venv\\Scripts\\Activate.ps1 # Windows (PowerShell)

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Running locally

```bash
uvicorn app.main:app --reload
```

## Environment variables

- `DATABASE_URL`: connection string for the database. Tests use a SQLite file if
  not provided.
- `CORS_ALLOW_ORIGINS`: comma-separated list of origins allowed by CORS.
  Defaults to `*` to permit any origin.

## API endpoints

The application exposes `/tasks` for CRUD operations on tasks persisted in the
configured database. Tasks may include nested `sub_tasks`, which are stored as
rows referencing their parent task. On startup, existing tables are dropped and
recreated automatically so the schema is always in sync with the models.
