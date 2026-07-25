Feature 1: Search + combine filters
mini ADR: # Architecture Decision Record: Search + Combined Filters for GET /tasks

## Status

Accepted

## Context

We are building a Task Tracker backend using FastAPI and Pydantic.
The system must support searching and filtering tasks through a single endpoint:

GET /tasks

The goal is to extend this endpoint to support:

* Text search (title + description)
* Combined filters (status, priority, assignee, optional tag/due_date)
* Input validation
* Clean, predictable API responses

This is a learning project, so the implementation must be simple, readable, and easy to run locally.

---

## Decision

We will implement all search and filtering logic inside the GET /tasks endpoint using query parameters and a service-layer filtering function.

### Query Parameters

The endpoint will support:

* search: str (optional)
* status: enum (ToDo, InProgress, Done)
* priority: enum (Low, Medium, High)
* assignee: str (optional)
* tag: str (optional, if implemented)
* due_date: date (optional, if implemented)

---

## Implementation Rules

### 1. Search Behavior

* Search applies to BOTH title and description
* Case-insensitive
* Partial matching allowed
* Logic: OR between title and description

Example:
search="api" → matches "API bug" and "fix api issue"

---

### 2. Filter Behavior

* Filters include: status, priority, assignee, tag, due_date
* ALL filters are combined using AND logic

Example:
status=ToDo AND priority=High AND assignee=John

---

### 3. Combined Search + Filters

* Search is applied FIRST (logical subset)
* Filters are applied AFTER
* Final result = tasks that satisfy ALL conditions

---

### 4. No Results Handling

* If no tasks match:

  * Return: []
  * Status: 200 OK
* Do NOT raise errors for empty results

---

### 5. Validation Rules

* status and priority must use enums
* Invalid values return:

  * 422 Unprocessable Entity
* Validation handled using FastAPI + Pydantic

---

## Suggested Implementation Structure

* Route Layer:

  * Parses query parameters
  * Calls service function

* Service Layer:

  * Applies search filtering
  * Applies field filters
  * Returns filtered list

Example flow:

1. Load all tasks
2. Apply search filter (if provided)
3. Apply status/priority/assignee filters
4. Return final list

---

## Consequences

### Positive

* Simple and easy to understand
* Clear separation of concerns (route vs logic)
* Fully satisfies all user stories

### Negative

* Filtering done in Python (not optimized)
* Not scalable for large datasets
* Limited realism compared to database queries

---

## Summary

The GET /tasks endpoint will:

* Accept multiple optional query parameters
* Apply search and filters using AND logic
* Return 200 OK with filtered results or empty list
* Reject invalid inputs with 422 errors

This approach prioritizes clarity and learning over optimization.
