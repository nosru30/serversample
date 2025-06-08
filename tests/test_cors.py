import os
from fastapi.testclient import TestClient

# Set environment variables for the app before import
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_cors.db")
os.environ["CORS_ALLOW_ORIGINS"] = "*"

from app.main import app

client = TestClient(app)


def test_cors_preflight_allows_any_origin():
    response = client.options(
        "/tasks/",
        headers={
            "Origin": "http://example.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    # When allow_credentials=True and allow_origins=["*"], Starlette returns the
    # requesting origin rather than "*".
    assert response.headers.get("access-control-allow-origin") == "http://example.com"
