import pytest

from ..src.tasks import extend_task_due_date


def test_delete_completed_tasks():
    task = {
        "id": 1,
        "title": "First",
        "description": "first desc",
        "priority": "Low",
        "category": "Work",
        "due_date": "2025-04-10",
        "completed": False,
        "created_at": "2025-01-10 17:54:10",
    }

    extend_task_due_date(task, 2)
    assert task.get("due_date") == "2025-04-12"
