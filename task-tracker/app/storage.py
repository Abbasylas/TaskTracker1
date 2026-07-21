import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.models import (
    CommentCreate,
    CommentResponse,
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)

DEFAULT_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tasks.json"


def _data_file() -> Path:
    configured = os.getenv("TASK_TRACKER_DATA_FILE")
    return Path(configured) if configured else DEFAULT_DATA_FILE


def load_data() -> dict:
    path = _data_file()
    if not path.exists() or path.stat().st_size == 0:
        return {"tasks": []}

    try:
        with path.open("r", encoding="utf-8") as file:
            loaded = json.load(file)
    except json.JSONDecodeError:
        return {"tasks": []}

    if isinstance(loaded, list):
        loaded = {"tasks": loaded}
    if not isinstance(loaded, dict) or not isinstance(loaded.get("tasks"), list):
        return {"tasks": []}

    for task in loaded["tasks"]:
        if isinstance(task, dict):
            task.setdefault("comments", [])
            task.pop("comment_count", None)
    return loaded


def save_data(data: dict) -> None:
    path = _data_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    temporary_path.replace(path)


def _task_response(task: dict) -> TaskResponse:
    comments = sorted(
        task.get("comments", []),
        key=lambda comment: datetime.fromisoformat(comment["created_at"].replace("Z", "+00:00")),
    )
    return TaskResponse(
        **{key: value for key, value in task.items() if key not in {"comments", "comment_count"}},
        comments=[CommentResponse.model_validate(comment) for comment in comments],
        comment_count=len(comments),
    )


def _find_task(data: dict, task_id: str) -> dict | None:
    return next((task for task in data["tasks"] if task.get("id") == task_id), None)


def add_task(payload: TaskCreate) -> TaskResponse:
    data = load_data()
    now = datetime.now(timezone.utc).isoformat()
    task = {
        "id": str(uuid4()),
        "title": payload.title,
        "description": payload.description or "",
        "status": payload.status.value,
        "priority": payload.priority.value,
        "assignee": payload.assignee,
        "tag": payload.tag,
        "due_date": payload.due_date.isoformat() if payload.due_date else None,
        "created_at": now,
        "updated_at": now,
        "comments": [],
    }
    data["tasks"].append(task)
    save_data(data)
    return _task_response(task)


def get_all_tasks() -> list[TaskResponse]:
    return [_task_response(task) for task in load_data()["tasks"]]


def get_task_by_id(task_id: str) -> TaskResponse | None:
    data = load_data()
    task = _find_task(data, task_id)
    return _task_response(task) if task else None


def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse | None:
    data = load_data()
    task = _find_task(data, task_id)
    if task is None:
        return None

    updates = payload.model_dump(exclude_unset=True, mode="json")
    if updates:
        task.update(updates)
        task["updated_at"] = datetime.now(timezone.utc).isoformat()
        save_data(data)
    return _task_response(task)


def delete_task(task_id: str) -> bool:
    data = load_data()
    original_length = len(data["tasks"])
    data["tasks"] = [task for task in data["tasks"] if task.get("id") != task_id]
    if len(data["tasks"]) == original_length:
        return False
    save_data(data)
    return True


def get_comments(task_id: str) -> list[CommentResponse] | None:
    task = _find_task(load_data(), task_id)
    if task is None:
        return None
    comments = sorted(
        task.setdefault("comments", []),
        key=lambda comment: datetime.fromisoformat(comment["created_at"].replace("Z", "+00:00")),
    )
    return [CommentResponse.model_validate(comment) for comment in comments]


def get_next_comment_id(data: dict) -> int:
    ids = [
        comment.get("id", 0)
        for task in data["tasks"]
        for comment in task.get("comments", [])
        if isinstance(comment.get("id"), int)
    ]
    return max(ids, default=0) + 1


def add_comment(task_id: str, payload: CommentCreate) -> CommentResponse | None:
    data = load_data()
    task = _find_task(data, task_id)
    if task is None:
        return None

    comment = {
        "id": get_next_comment_id(data),
        "text": payload.text,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    task.setdefault("comments", []).append(comment)
    task["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_data(data)
    return CommentResponse.model_validate(comment)


def delete_comment(task_id: str, comment_id: int) -> bool | None:
    data = load_data()
    task = _find_task(data, task_id)
    if task is None:
        return None

    comments = task.setdefault("comments", [])
    remaining = [comment for comment in comments if comment.get("id") != comment_id]
    if len(remaining) == len(comments):
        return False

    task["comments"] = remaining
    task["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_data(data)
    return True


def _reset() -> None:
    save_data({"tasks": []})
