"""Six break tests: three for comments and three for search/combined filters."""


# Feature 1: Task comments (3 tests)

def test_comments_can_be_added_and_listed(client, task):
    created = client.post(
        f"/tasks/{task['id']}/comments",
        json={"text": "First break-test comment"},
    )
    listed = client.get(f"/tasks/{task['id']}/comments")

    assert created.status_code == 201
    assert listed.status_code == 200
    assert listed.json() == [created.json()]


def test_blank_comment_is_rejected(client, task):
    response = client.post(
        f"/tasks/{task['id']}/comments",
        json={"text": "   "},
    )

    assert response.status_code == 422


def test_comment_count_updates_after_add(client, task):
    client.post(f"/tasks/{task['id']}/comments", json={"text": "Count this"})
    response = client.get(f"/tasks/{task['id']}")

    assert response.status_code == 200
    assert response.json()["comment_count"] == 1


# Feature 2: Search and combined filters (3 tests)

def test_search_matches_title_and_description(client, task):
    client.post(
        "/tasks",
        json={"title": "Documentation", "description": "Explains the api filters"},
    )

    response = client.get("/tasks", params={"search": "API"})

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_combined_filters_return_only_the_full_match(client, task):
    client.post(
        "/tasks",
        json={
            "title": "Similar but low priority",
            "status": "ToDo",
            "priority": "Low",
            "assignee": "John",
            "tag": "backend",
            "due_date": "2026-07-22",
        },
    )

    response = client.get(
        "/tasks",
        params={
            "status": "ToDo",
            "priority": "High",
            "assignee": "john",
            "tag": "BACKEND",
            "due_date": "2026-07-22",
        },
    )

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [task["id"]]


def test_invalid_filter_value_returns_422(client, task):
    response = client.get("/tasks", params={"status": "Blocked"})

    assert response.status_code == 422
