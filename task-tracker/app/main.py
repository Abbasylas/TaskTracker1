"""Task Tracker FastAPI application."""

from datetime import date, datetime, timezone

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.business_rules import validate_status_transition
from app.models import (
    CommentCreate,
    CommentResponse,
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)
from app.services import filter_tasks

app = FastAPI(
    title="Task Tracker API",
    description="A learning-focused REST API for tracking tasks, built with FastAPI.",
    version="0.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8001",
        "http://127.0.0.1:8001",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type"],
)


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    search: str | None = None,
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    assignee: str | None = None,
    tag: str | None = None,
    due_date: date | None = None,
) -> list[TaskResponse]:
    tasks = storage.get_all_tasks()
    return filter_tasks(
        tasks,
        search=search,
        status=status,
        priority=priority,
        assignee=assignee,
        tag=tag,
        due_date=due_date,
    )


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        validate_status_transition(existing.status, payload.status)

    updated = storage.update_task(task_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> Response:
    if not storage.delete_task(task_id):
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post(
    "/tasks/{task_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["comments"],
)
def create_comment(task_id: str, payload: CommentCreate) -> CommentResponse:
    comment = storage.add_comment(task_id, payload)
    if comment is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return comment


@app.get("/tasks/{task_id}/comments", response_model=list[CommentResponse], tags=["comments"])
def list_comments(task_id: str) -> list[CommentResponse]:
    comments = storage.get_comments(task_id)
    if comments is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return comments


@app.delete(
    "/tasks/{task_id}/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["comments"],
)
def remove_comment(task_id: str, comment_id: int) -> Response:
    result = storage.delete_comment(task_id, comment_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if result is False:
        raise HTTPException(status_code=404, detail="Comment not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
