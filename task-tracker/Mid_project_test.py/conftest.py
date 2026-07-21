import pytest
from fastapi.testclient import TestClient

from app import storage
from app.main import app


@pytest.fixture(autouse=True)
def isolated_break_test_storage(tmp_path, monkeypatch):
    test_file = tmp_path / "mid_project_tasks.json"
    monkeypatch.setenv("TASK_TRACKER_DATA_FILE", str(test_file))
    storage._reset()
    yield
    storage._reset()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def task(client: TestClient) -> dict:
    response = client.post(
        "/tasks",
        json={
            "title": "API break-test task",
            "description": "Used to test comments and filters",
            "status": "ToDo",
            "priority": "High",
            "assignee": "John",
            "tag": "backend",
            "due_date": "2026-07-22",
        },
    )
    assert response.status_code == 201
    return response.json()
