import os

import pytest
from fastapi.testclient import TestClient

from app import storage
from app.main import app


@pytest.fixture(autouse=True)
def isolated_storage(tmp_path, monkeypatch):
    test_file = tmp_path / "tasks.json"
    monkeypatch.setenv("TASK_TRACKER_DATA_FILE", str(test_file))
    storage._reset()
    yield
    storage._reset()
    monkeypatch.delenv("TASK_TRACKER_DATA_FILE", raising=False)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def created_task(client: TestClient) -> dict:
    response = client.post("/tasks", json={"title": "fixture task"})
    assert response.status_code == 201
    return response.json()
