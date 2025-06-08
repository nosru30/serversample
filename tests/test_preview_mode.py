import os
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test_preview.db"
os.environ["PREVIEW_MODE"] = "1"

from app.main import app
from app.db import SessionLocal, UserORM


def test_preview_user_seeded():
    with TestClient(app) as client:
        session = SessionLocal()
        try:
            user = (
                session.query(UserORM)
                .filter(UserORM.email == "demo@example.com")
                .first()
            )
            assert user is not None
        finally:
            session.close()

        r = client.post(
            "/login",
            json={"email": "demo@example.com", "password": "demo"},
        )
        assert r.status_code == 200

