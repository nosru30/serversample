import os
import sqlalchemy
import pytest

pg_url = os.getenv("DATABASE_URL")
if not pg_url:
    pytest.skip('DATABASE_URL not set, skipping Postgres tests', allow_module_level=True)

from fastapi.testclient import TestClient
from app.db import Base, engine, SessionLocal
from app.db_models import TaskORM
from app.main import app


def test_postgres_migration_and_crud():
    pg_url = os.getenv("DATABASE_URL")
    if not pg_url:
        pytest.skip('DATABASE_URL not set, skipping Postgres tests')

    # Ensure clean slate
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    insp = sqlalchemy.inspect(engine)
    assert insp.has_table('tasks')

    # verify the app connected using the provided DATABASE_URL
    assert engine.url.database == sqlalchemy.engine.url.make_url(pg_url).database

    client = TestClient(app)
    payload = {'title': 'PG Task from test'}
    r = client.post('/dbtasks/', json=payload)
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

