import os
import uuid
import pytest
from fastapi.testclient import TestClient

# Ensure DATABASE_URL points to a reachable database. These tests will skip if
# the variable isn't provided.
pg_url = os.getenv("DATABASE_URL")
if not pg_url:
    pytest.skip("DATABASE_URL not set, skipping DB tests", allow_module_level=True)

from app.main import app
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

client = TestClient(app)

created_task_id = None

def test_create_db_task():
    global created_task_id
    payload = {
        "title": "DB Task",
        "description": "stored in db",
    }
    response = client.post("/dbtasks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    created_task_id = uuid.UUID(data["id"])
    assert data["title"] == payload["title"]


def test_read_db_tasks():
    response = client.get("/dbtasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(task["id"] == str(created_task_id) for task in data)


def test_update_db_task():
    payload = {
        "title": "Updated DB Task",
        "description": "updated",
        "priority": 2,
        "completed": True,
    }
    response = client.put(f"/dbtasks/{created_task_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["completed"] is True


def test_delete_db_task():
    response = client.delete(f"/dbtasks/{created_task_id}")
    assert response.status_code == 204
    get_response = client.get(f"/dbtasks/{created_task_id}")
    assert get_response.status_code == 404
