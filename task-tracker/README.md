# Task Tracker API

A learning-focused REST API for tracking tasks, built with **Python**, **FastAPI**, and **Pydantic**.

This project is intentionally minimal at this stage. Per the current architecture
decision, it uses **in-memory storage with JSON file persistence** (no database,
no authentication, no Docker) to keep the focus on REST API design, validation,
and frontend-backend interaction.

> **Current scope:** This skeleton only includes the application setup and a
> `/health` endpoint. Task CRUD endpoints will be added in a later module.

---

## Project Structure

```
task-tracker/
├── app/
│   ├── __init__.py
│   └── main.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Prerequisites

* Python 3.10+ installed
* `pip` available on your PATH

---

## Setup Instructions

1. **Clone or copy this project locally**, then move into the project folder:

   ```bash
   cd task-tracker
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   ```

   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

   On Windows (PowerShell):
   ```bash
   venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create your local environment file:**

   Copy `.env.example` to `.env` and adjust values if needed:

   ```bash
   cp .env.example .env
   ```

   (On Windows, use `copy .env.example .env`.)

---

## Running the Application

Start the development server with Uvicorn (auto-reload enabled):

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:

```
http://127.0.0.1:8000
```

---

## Testing the /health Endpoint

With the server running, test the health check endpoint using `curl`:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "timestamp": "2026-07-03T12:00:00.000000+00:00"
}
```

---

## Interactive API Docs (Swagger UI)

FastAPI automatically generates interactive API documentation. Once the
server is running, open your browser to:

```
http://127.0.0.1:8000/docs
```

You can also view the alternative ReDoc documentation at:

```
http://127.0.0.1:8000/redoc
```

---

## Notes

* The dependency versions in `requirements.txt` are known-good pins at the
  time of writing. After installing, it's good practice to verify the
  exact versions resolved in your environment with `pip freeze` and adjust
  the file if needed.
* No CRUD endpoints, database, authentication, or frontend are included in
  this skeleton by design — see the project's Architecture Decision Record
  for the planned evolution of this project.
