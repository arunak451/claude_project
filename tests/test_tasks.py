import os
import tempfile
import unittest

from task_manager.app import create_app


class TaskApiTests(unittest.TestCase):
    def setUp(self):
        fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        self.app = create_app(self.db_path)
        self.client = self.app.test_client()

    def tearDown(self):
        os.remove(self.db_path)

    def _create(self, title, **extra):
        return self.client.post("/tasks", json={"title": title, **extra})

    def test_create_task(self):
        res = self._create("Write report")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()["title"], "Write report")

    def test_create_task_requires_title(self):
        res = self.client.post("/tasks", json={"title": "  "})
        self.assertEqual(res.status_code, 400)

    def test_get_missing_task_returns_404(self):
        res = self.client.get("/tasks/999")
        self.assertEqual(res.status_code, 404)

    def test_complete_task(self):
        task_id = self._create("Pay bills").get_json()["id"]
        res = self.client.post(f"/tasks/{task_id}/complete")
        self.assertTrue(res.get_json()["completed"])

    def test_first_page_returns_first_tasks(self):
        for i in range(5):
            self._create(f"Task {i}")
        res = self.client.get("/tasks?page=1&page_size=2")
        titles = [t["title"] for t in res.get_json()]
        self.assertEqual(titles, ["Task 0", "Task 1"])


if __name__ == "__main__":
    unittest.main()
