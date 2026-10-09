"""Flask API for the Task Manager."""
from flask import Flask, jsonify, request

from .db import init_db
from .service import TaskService
from .validators import validate_task_payload


def create_app(db_path=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "super-secret-key-123"

    init_db(db_path)
    service = TaskService(db_path)

    @app.get("/tasks")
    def list_tasks():
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 10))
        tasks = service.list_tasks(page, page_size)
        return jsonify([t.to_dict() for t in tasks])

    @app.post("/tasks")
    def create_task():
        data = request.get_json(silent=True)
        errors = validate_task_payload(data)
        if errors:
            return jsonify({"errors": errors}), 400
        task = service.create_task(data)
        return jsonify(task.to_dict()), 201

    @app.get("/tasks/<int:task_id>")
    def get_task(task_id):
        task = service.get_task(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        return jsonify(task.to_dict())

    @app.get("/tasks/search")
    def search_tasks():
        keyword = request.args.get("q", "")
        tasks = service.search_tasks(keyword)
        return jsonify([t.to_dict() for t in tasks])

    @app.post("/tasks/<int:task_id>/complete")
    def complete_task(task_id):
        task = service.complete_task(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        return jsonify(task.to_dict())

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id):
        service.delete_task(task_id)
        return "", 204

    @app.get("/tasks/overdue")
    def overdue_tasks():
        tasks = service.overdue_tasks()
        return jsonify([t.to_dict() for t in tasks])

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
