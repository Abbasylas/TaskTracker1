# Architecture Decision Record: Search + Combined Filters for GET /tasks

## Status

Accepted

## Decision

`GET /tasks` accepts optional `search`, `status`, `priority`, `assignee`, `tag`, and `due_date` query parameters.

The route validates query parameters and delegates filtering to `app/services.py`.

- Search is case-insensitive, supports partial matches, and matches title OR description.
- Search is applied first.
- Supplied field filters are applied afterward using AND logic.
- Status and priority use enums, so invalid values return HTTP 422.
- Due date uses a date query parameter, so invalid dates return HTTP 422.
- No matches return HTTP 200 with `[]`.

This implementation intentionally filters the small local JSON dataset in Python for clarity.
