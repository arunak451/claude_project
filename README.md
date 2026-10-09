# Task Manager API

A small Flask + SQLite REST API for managing tasks.

## Setup

```bash
python -m venv venv
# Windows: venv\Scripts\activate    Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python -m task_manager.app
```

The API runs at http://127.0.0.1:5000

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | /tasks?page=1&page_size=10 | List tasks |
| POST | /tasks | Create a task (`title`, `description`, `due_date`) |
| GET | /tasks/<id> | Get one task |
| GET | /tasks/search?q=word | Search tasks by title |
| POST | /tasks/<id>/complete | Mark a task complete |
| DELETE | /tasks/<id> | Delete a task |
| GET | /tasks/overdue | List overdue tasks |

## Tests

```bash
python -m pytest
```
