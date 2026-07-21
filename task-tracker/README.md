# Task Tracker

## Running Backend

cd C:\Users\Lenovo\Downloads\task-tracker-mid-project\task-tracker

### 1. First-time setup

Create a virtual environment:

```bash
py -3.14 -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

You only need to create the environment and install the packages once.

Backend:

From the main `task-tracker` folder, run:

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Running the frontend

Keep the backend terminal running. Open a second CMD or VS Code terminal.

Move into the frontend folder:

```bash
cd C:\Users\Lenovo\Downloads\task-tracker-mid-project\task-tracker\frontend
```

Start the frontend server:

```bash
py -3.14 -m http.server 8001
```

Open: http://127.0.0.1:8001/

## Running Tests for the New Features

The two new features are:

- Task search and combined filters
- Task comments

Their test files are:

```text
tests/test_search_filters.py
tests/test_comments.py
```

Run Tests for Both New Features

```bash
python -m pytest tests/test_search_filters.py tests/test_comments.py -v
```

Run Only the Search and Filter Tests

```bash
python -m pytest tests/test_search_filters.py -v
```

Run Only the Comment Tests

```bash
python -m pytest tests/test_comments.py -v
```

### Run an Individual Search Test

```bash
python -m pytest tests/test_search_filters.py::test_search_matches_title_or_description_case_insensitively -v
```

### Run an Individual Comment Test

```bash
python -m pytest tests/test_comments.py::test_add_valid_comment_returns_201 -v
```

### Run the Complete Backend Test Suite

Run every backend test to confirm that the new features have not broken existing functionality:

```bash
python -m pytest -v
```
