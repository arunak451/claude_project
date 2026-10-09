"""Input validation helpers."""
from datetime import datetime


def validate_task_payload(data):
    """Return a list of error messages. Empty list means valid."""
    errors = []
    if not data:
        return ["Request body is required"]

    title = data.get("title")
    if not title or not title.strip():
        errors.append("Title is required")
    elif len(title) > 100:
        errors.append("Title must be 100 characters or less")

    due_date = data.get("due_date")
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            errors.append("due_date must be in YYYY-MM-DD format")

    return errors
