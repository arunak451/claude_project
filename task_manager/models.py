"""Task model."""
from datetime import datetime, date


class Task:
    def __init__(self, id, title, description=None, due_date=None,
                 completed=False, created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = bool(completed)
        self.created_at = created_at

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            due_date=row["due_date"],
            completed=row["completed"],
            created_at=row["created_at"],
        )

    def is_overdue(self):
        if not self.due_date:
            return False
        due = datetime.strptime(self.due_date, "%Y-%m-%d").date()
        return due < date.today()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "completed": self.completed,
            "created_at": self.created_at,
            "overdue": self.is_overdue(),
        }
