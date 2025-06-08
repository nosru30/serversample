import os
import sqlalchemy
import pytest

pg_url = os.getenv("DATABASE_URL")
if not pg_url or not pg_url.startswith("postgres"):
    pytest.skip('DATABASE_URL not set to Postgres, skipping Postgres tests', allow_module_level=True)

from fastapi.testclient import TestClient
from app.db import Base, engine, SessionLocal, TaskORM
from app.main import app
from app.migrate import run_migrations


def test_postgres_migration_and_crud():
    pg_url = os.getenv("DATABASE_URL")
    if not pg_url:
        pytest.skip('DATABASE_URL not set, skipping Postgres tests')

    # Ensure clean slate
    Base.metadata.drop_all(bind=engine)
    run_migrations()

    insp = sqlalchemy.inspect(engine)
    assert insp.has_table('tasks')

    # verify the app connected using the provided DATABASE_URL
    assert engine.url.database == sqlalchemy.engine.url.make_url(pg_url).database

    client = TestClient(app)
    payload = {'title': 'PG Task from test'}
    r = client.post('/tasks/', json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data['title'] == payload['title']

    # Verify directly via session
    session = SessionLocal()
    try:
        count = session.query(TaskORM).count()
        assert count == 1
    finally:
        session.close()

    # Cleanup tables after test
    Base.metadata.drop_all(bind=engine)

