from fastapi.testclient import TestClient


def create_task(
    client: TestClient,
    *,
    title: str,
    description: str = "",
    status: str = "ToDo",
    priority: str = "Medium",
    assignee: str | None = None,
    tag: str | None = None,
    due_date: str | None = None,
) -> dict:
    response = client.post(
        "/tasks",
        json={
            "title": title,
            "description": description,
            "status": status,
            "priority": priority,
            "assignee": assignee,
            "tag": tag,
            "due_date": due_date,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_search_matches_title_or_description_case_insensitively(client):
    create_task(client, title="API Bug", description="Authentication failure")
    create_task(client, title="Update docs", description="Explain the api query parameters")
    create_task(client, title="Style cards", description="Improve spacing")

    response = client.get("/tasks", params={"search": "aPi"})

    assert response.status_code == 200
    assert {task["title"] for task in response.json()} == {"API Bug", "Update docs"}


def test_combined_filters_use_and_logic(client):
    create_task(client, title="Match", status="ToDo", priority="High", assignee="John")
    create_task(client, title="Wrong priority", status="ToDo", priority="Low", assignee="John")
    create_task(client, title="Wrong assignee", status="ToDo", priority="High", assignee="Sara")

    response = client.get(
        "/tasks",
        params={"status": "ToDo", "priority": "High", "assignee": "john"},
    )

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Match"]


def test_search_is_applied_with_tag_and_due_date_filters(client):
    create_task(
        client,
        title="Fix API endpoint",
        description="Backend work",
        priority="High",
        tag="backend",
        due_date="2026-07-22",
    )
    create_task(
        client,
        title="Fix API page",
        description="Frontend work",
        priority="High",
        tag="frontend",
        due_date="2026-07-22",
    )

    response = client.get(
        "/tasks",
        params={
            "search": "api",
            "priority": "High",
            "tag": "BACKEND",
            "due_date": "2026-07-22",
        },
    )

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Fix API endpoint"]


def test_no_matches_returns_empty_list_with_200(client):
    create_task(client, title="Existing task")

    response = client.get("/tasks", params={"search": "not-present"})

    assert response.status_code == 200
    assert response.json() == []


def test_invalid_status_and_priority_return_422(client):
    assert client.get("/tasks", params={"status": "Blocked"}).status_code == 422
    assert client.get("/tasks", params={"priority": "Urgent"}).status_code == 422


def test_invalid_due_date_returns_422(client):
    response = client.get("/tasks", params={"due_date": "tomorrow"})

    assert response.status_code == 422
