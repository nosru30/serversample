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


@pytest.fixture(autouse=True)
def ensure_tables():
    Base.metadata.create_all(bind=engine)

client = TestClient(app)

created_task_id = None

def test_create_task():
    global created_task_id
    payload = {
        "title": "DB Task",
        "description": "stored in db",
        "sub_tasks": [
            {"title": "sub", "description": "child"}
        ],
    }
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    created_task_id = uuid.UUID(data["id"])
    assert data["title"] == payload["title"]
    assert len(data["sub_tasks"]) == 1


def test_read_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    match = next((t for t in data if t["id"] == str(created_task_id)), None)
    assert match is not None
    assert len(match["sub_tasks"]) == 1


def test_update_task():
    payload = {
        "title": "Updated DB Task",
        "description": "updated",
        "priority": 2,
        "completed": True,
        "sub_tasks": [
            {"title": "new sub", "description": "child 2"}
        ],
    }
    response = client.put(f"/tasks/{created_task_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["completed"] is True
    assert len(data["sub_tasks"]) == 1


def test_delete_task():
    response = client.delete(f"/tasks/{created_task_id}")
    assert response.status_code == 204
    get_response = client.get(f"/tasks/{created_task_id}")
    assert get_response.status_code == 404
