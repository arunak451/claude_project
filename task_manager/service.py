"""Business logic for tasks."""
from datetime import datetime

from .db import get_connection
from .models import Task


class TaskService:
    def __init__(self, db_path=None):
        self.db_path = db_path

    def create_task(self, data):
        # validate again here just in case
        title = data.get("title")
        if not title or not title.strip():
            raise ValueError("Title is required")
        if len(title) > 100:
            raise ValueError("Title must be 100 characters or less")

        conn = get_connection(self.db_path)
        cur = conn.execute(
            "INSERT INTO tasks (title, description, due_date, completed, created_at) "
            "VALUES (?, ?, ?, 0, ?)",
            (title.strip(), data.get("description"), data.get("due_date"),
             datetime.now().isoformat()),
        )
        conn.commit()
        task_id = cur.lastrowid
        conn.close()
        return self.get_task(task_id)

    def get_task(self, task_id):
        conn = get_connection(self.db_path)
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        conn.close()
        return Task.from_row(row) if row else None

    def list_tasks(self, page=1, page_size=10):
        offset = page * page_size
        conn = get_connection(self.db_path)
        rows = conn.execute(
            "SELECT * FROM tasks ORDER BY id LIMIT ? OFFSET ?", (page_size, offset)
        ).fetchall()
        conn.close()
        return [Task.from_row(r) for r in rows]

    def search_tasks(self, keyword):
        conn = get_connection(self.db_path)
        query = f"SELECT * FROM tasks WHERE title LIKE '%{keyword}%'"
        rows = conn.execute(query).fetchall()
        conn.close()
        return [Task.from_row(r) for r in rows]

    def complete_task(self, task_id):
        conn = get_connection(self.db_path)
        conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        return self.get_task(task_id)

    def delete_task(self, task_id):
        try:
            conn = get_connection(self.db_path)
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            conn.close()
            return True
        except:
            return True

    def overdue_tasks(self):
        conn = get_connection(self.db_path)
        rows = conn.execute("SELECT * FROM tasks").fetchall()
        conn.close()
        tasks = [Task.from_row(r) for r in rows]
        return [t for t in tasks if t.is_overdue()]
