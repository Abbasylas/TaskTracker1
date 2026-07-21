"""Simple business services for task search and combined filtering."""

from datetime import date

from app.models import TaskPriority, TaskResponse, TaskStatus


def filter_tasks(
    tasks: list[TaskResponse],
    *,
    search: str | None = None,
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    assignee: str | None = None,
    tag: str | None = None,
    due_date: date | None = None,
) -> list[TaskResponse]:
    """Return tasks matching search first, then every supplied filter.

    Search is case-insensitive and uses OR logic across title and description.
    Field filters are combined using AND logic.
    """

    filtered = tasks

    cleaned_search = search.strip().casefold() if search else ""
    if cleaned_search:
        filtered = [
            task
            for task in filtered
            if cleaned_search in task.title.casefold()
            or cleaned_search in (task.description or "").casefold()
        ]

    if status is not None:
        filtered = [task for task in filtered if task.status == status]

    if priority is not None:
        filtered = [task for task in filtered if task.priority == priority]

    cleaned_assignee = assignee.strip().casefold() if assignee else ""
    if cleaned_assignee:
        filtered = [
            task
            for task in filtered
            if task.assignee is not None and task.assignee.casefold() == cleaned_assignee
        ]

    cleaned_tag = tag.strip().casefold() if tag else ""
    if cleaned_tag:
        filtered = [
            task
            for task in filtered
            if task.tag is not None and task.tag.casefold() == cleaned_tag
        ]

    if due_date is not None:
        filtered = [task for task in filtered if task.due_date == due_date]

    return filtered
