import os
import datetime
import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test_attendance.db"

from app.main import app
from app.db import (
    Base,
    engine,
    SessionLocal,
    RoleORM,
    UserORM,
    EmployeeORM,
)
from app.migrate import run_migrations
from app import auth

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_data():
    run_migrations()
    session = SessionLocal()
    try:
        role = RoleORM(name="employee")
        session.add(role)
        session.commit()
        user = UserORM(email="user@example.com", password=auth.hash_password("pass"), role_id=role.id)
        session.add(user)
        session.commit()
        emp = EmployeeORM(user_id=user.id, employee_id="E001", name="Test User")
        session.add(emp)
        session.commit()
    finally:
        session.close()


def test_login_and_me():
    response = client.post("/login", json={"email": "user@example.com", "password": "pass"})
    assert response.status_code == 200
    token = response.json()["token"]
    me = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "user@example.com"


def test_attendance_crud():
    login = client.post("/login", json={"email": "user@example.com", "password": "pass"})
    token = login.json()["token"]
    payload = {
        "date": "2024-01-01",
        "start_time": "2024-01-01T09:00:00Z",
        "end_time": "2024-01-01T17:00:00Z",
        "break_duration_minutes": 60,
        "notes_free_text": "work",
    }
    r = client.post("/attendances", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 201
    att_id = r.json()["id"]

    # update the same day
    updated = payload.copy()
    updated["start_time"] = "2024-01-01T10:00:00Z"
    r2 = client.post("/attendances", json=updated, headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    assert r2.json()["id"] == att_id
    assert r2.json()["start_time"].startswith("2024-01-01T10:00:00")
    month = client.get("/attendances?month=2024-01", headers={"Authorization": f"Bearer {token}"})
    assert month.status_code == 200
    assert len(month.json()) == 1
    assert month.json()[0]["start_time"].startswith("2024-01-01T10:00:00")
    d = client.delete(f"/attendances/{att_id}", headers={"Authorization": f"Bearer {token}"})
    assert d.status_code == 204
