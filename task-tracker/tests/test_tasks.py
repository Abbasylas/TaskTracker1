def test_cors_preflight_allows_localhost_frontend(client):
    response = client.options(
        "/tasks",
        headers={
            "Origin": "http://localhost:8080",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:8080"


def test_create_task_valid_returns_201_with_full_body(client):
    response = client.post(
        "/tasks",
        json={
            "title": "  Buy milk  ",
            "description": "2% organic",
            "status": "ToDo",
            "priority": "High",
            "assignee": "alice",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Buy milk"
    assert body["description"] == "2% organic"
    assert body["status"] == "ToDo"
    assert body["priority"] == "High"
    assert body["assignee"] == "alice"
    assert isinstance(body["id"], str) and body["id"]
    assert body["created_at"]
    assert body["updated_at"]


def test_create_task_missing_title_returns_422(client):
    response = client.post("/tasks", json={"description": "no title"})

    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client):
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    response = client.post("/tasks", json={"title": "Valid", "priority": "Urgent"})

    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    response = client.post("/tasks", json={"title": "Valid", "foo": "bar"})

    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client):
    client.post("/tasks", json={"title": "Task A", "status": "ToDo"})

    response = client.get("/tasks", params={"status": "Done"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    client.post("/tasks", json={"title": "High task", "priority": "High"})
    client.post("/tasks", json={"title": "Low task", "priority": "Low"})
    client.post("/tasks", json={"title": "Another high", "priority": "High"})

    response = client.get("/tasks", params={"priority": "High"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert all(task["priority"] == "High" for task in body)


def test_get_task_by_id_returns_task(client, created_task):
    response = client.get(f"/tasks/{created_task['id']}")

    assert response.status_code == 200
    assert response.json() == created_task


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    task_id = "missing-task-id"
    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {task_id} not found"


def test_patch_partial_update_keeps_other_fields(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"title": "updated title"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "updated title"
    assert body["status"] == created_task["status"]
    assert body["priority"] == created_task["priority"]
    assert body["description"] == created_task["description"]
    assert body["assignee"] == created_task["assignee"]
    assert body["id"] == created_task["id"]


def test_patch_not_found_returns_404(client):
    response = client.patch(
        "/tasks/missing-task-id",
        json={"title": "does not matter"},
    )

    assert response.status_code == 404


def test_patch_empty_body_returns_200_and_leaves_task_unchanged(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Original task",
            "description": "Keep me",
            "status": "ToDo",
            "priority": "Medium",
            "assignee": "alice",
        },
    )

    assert create_response.status_code == 201
    created_task = create_response.json()

    response = client.patch(f"/tasks/{created_task['id']}", json={})

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == created_task["id"]
    assert body["title"] == created_task["title"]
    assert body["description"] == created_task["description"]
    assert body["status"] == created_task["status"]
    assert body["priority"] == created_task["priority"]
    assert body["assignee"] == created_task["assignee"]


def test_patch_unknown_field_returns_422(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Original task",
            "description": "Keep me",
            "status": "ToDo",
            "priority": "Medium",
            "assignee": "alice",
        },
    )

    assert create_response.status_code == 201
    created_task = create_response.json()

    response = client.patch(f"/tasks/{created_task['id']}", json={"foo": "bar"})

    assert response.status_code == 422
    body = response.json()
    assert body["detail"]


def test_patch_blank_title_returns_422(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Original task",
            "description": "Keep me",
            "status": "ToDo",
            "priority": "Medium",
            "assignee": "alice",
        },
    )

    assert create_response.status_code == 201
    created_task = create_response.json()

    response = client.patch(f"/tasks/{created_task['id']}", json={"title": "   "})

    assert response.status_code == 422
    body = response.json()
    assert body["detail"]


def test_patch_explicit_null_title_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"title": None},
    )

    assert response.status_code == 422
    body = response.json()
    assert body["detail"]


def test_patch_title_too_long_returns_422(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Original task",
            "description": "Keep me",
            "status": "ToDo",
            "priority": "Medium",
            "assignee": "alice",
        },
    )

    assert create_response.status_code == 201
    created_task = create_response.json()

    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"title": "x" * 201},
    )

    assert response.status_code == 422
    body = response.json()
    assert body["detail"]


def test_patch_invalid_priority_returns_422(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Original task",
            "description": "Keep me",
            "status": "ToDo",
            "priority": "Medium",
            "assignee": "alice",
        },
    )

    assert create_response.status_code == 201
    created_task = create_response.json()

    response = client.patch(f"/tasks/{created_task['id']}", json={"priority": "Urgent"})

    assert response.status_code == 422
    body = response.json()
    assert body["detail"]


def test_patch_malformed_json_returns_422(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Original task",
            "description": "Keep me",
            "status": "ToDo",
            "priority": "Medium",
            "assignee": "alice",
        },
    )

    assert create_response.status_code == 201
    created_task = create_response.json()

    response = client.patch(
        f"/tasks/{created_task['id']}",
        content='{"title":',
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 422
    body = response.json()
    assert body["detail"]


def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "InProgress"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "Done"},
    )

    assert response.status_code == 422


def test_patch_same_status_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "ToDo"},
    )

    assert response.status_code == 422


def test_delete_existing_returns_204_no_body(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    response = client.delete("/tasks/missing-task-id")

    assert response.status_code == 404
