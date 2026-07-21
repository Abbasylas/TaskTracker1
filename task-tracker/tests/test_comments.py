from datetime import datetime


def create_task(client, title="Task"):
    response = client.post("/tasks", json={"title": title})
    assert response.status_code == 201
    return response.json()


def test_add_valid_comment_returns_201(client, created_task):
    response = client.post(f"/tasks/{created_task['id']}/comments", json={"text": "Started work"})
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["text"] == "Started work"
    assert datetime.fromisoformat(body["created_at"])


def test_missing_comment_text_returns_422(client, created_task):
    assert client.post(f"/tasks/{created_task['id']}/comments", json={}).status_code == 422


def test_empty_comment_text_returns_422(client, created_task):
    assert client.post(f"/tasks/{created_task['id']}/comments", json={"text": ""}).status_code == 422


def test_whitespace_comment_text_returns_422(client, created_task):
    assert client.post(f"/tasks/{created_task['id']}/comments", json={"text": "   "}).status_code == 422


def test_add_comment_to_missing_task_returns_404(client):
    response = client.post("/tasks/missing/comments", json={"text": "Hello"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_get_comments_returns_comments_oldest_first(client, created_task):
    first = client.post(f"/tasks/{created_task['id']}/comments", json={"text": "First"}).json()
    second = client.post(f"/tasks/{created_task['id']}/comments", json={"text": "Second"}).json()
    response = client.get(f"/tasks/{created_task['id']}/comments")
    assert response.status_code == 200
    assert response.json() == [first, second]


def test_get_comments_for_task_without_comments_returns_empty_list(client, created_task):
    response = client.get(f"/tasks/{created_task['id']}/comments")
    assert response.status_code == 200
    assert response.json() == []


def test_get_comments_for_missing_task_returns_404(client):
    response = client.get("/tasks/missing/comments")
    assert response.status_code == 404


def test_delete_existing_comment_returns_204_and_removes_it(client, created_task):
    comment = client.post(f"/tasks/{created_task['id']}/comments", json={"text": "Delete me"}).json()
    response = client.delete(f"/tasks/{created_task['id']}/comments/{comment['id']}")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/tasks/{created_task['id']}/comments").json() == []


def test_delete_missing_comment_returns_404(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}/comments/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Comment not found"


def test_delete_comment_from_missing_task_returns_404(client):
    response = client.delete("/tasks/missing/comments/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_comment_count_increases_and_decreases(client, created_task):
    task_id = created_task["id"]
    assert client.get(f"/tasks/{task_id}").json()["comment_count"] == 0
    comment = client.post(f"/tasks/{task_id}/comments", json={"text": "Count me"}).json()
    assert client.get(f"/tasks/{task_id}").json()["comment_count"] == 1
    client.delete(f"/tasks/{task_id}/comments/{comment['id']}")
    assert client.get(f"/tasks/{task_id}").json()["comment_count"] == 0


def test_comment_ids_are_unique_across_tasks(client):
    first_task = create_task(client, "First")
    second_task = create_task(client, "Second")
    first_comment = client.post(f"/tasks/{first_task['id']}/comments", json={"text": "One"}).json()
    second_comment = client.post(f"/tasks/{second_task['id']}/comments", json={"text": "Two"}).json()
    assert first_comment["id"] == 1
    assert second_comment["id"] == 2


def test_task_list_includes_comment_count(client, created_task):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json()[0]["comment_count"] == 0
    assert response.json()[0]["comments"] == []
