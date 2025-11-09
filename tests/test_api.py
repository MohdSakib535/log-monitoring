import os
os.environ["APP_ENV"] = "testing"

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_ingest_log_accepts():
    payload = {"level": "INFO", "message": "hello", "service_name": "test"}
    r = client.post("/logs/", json=payload)
    # In testing, task applies locally, so should accept
    assert r.status_code == 202
    assert r.json()["status"] == "queued"

