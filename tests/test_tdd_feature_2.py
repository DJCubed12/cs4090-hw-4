import pytest

from ..src.tasks import sort_by_due_date


@pytest.fixture
def tasks():
    return [
        {
            "id": 1,
            "title": "First",
            "description": "first desc",
            "priority": "Low",
            "category": "Work",
            "due_date": "2025-04-10",
            "completed": False,
            "created_at": "2025-01-10 17:54:10",
        },
        {
            "id": 2,
            "title": "Second",
            "description": "description",
            "priority": "Medium",
            "category": "Personal",
            "due_date": "2025-02-10",
            "completed": True,
            "created_at": "2025-01-10 17:54:16",
        },
        {
            "id": 3,
            "title": "Third",
            "description": "",
            "priority": "High",
            "category": "Other",
            "due_date": "2025-07-10",
            "completed": False,
            "created_at": "2025-01-10 17:54:16",
        },
        {
            "id": 4,
            "title": "Fourth",
            "description": "the last one",
            "priority": "High",
            "category": "School",
            "due_date": "2025-05-10",
            "completed": True,
            "created_at": "2025-01-10 17:54:16",
        },
    ]


def test_sort_by_due_date(tasks):
    original_len = len(tasks)
    sorted_tasks = sort_by_due_date(tasks)

    assert len(sorted_tasks) == original_len

    for i in range(original_len - 1):
        assert sorted_tasks[i].get("due_date") < sorted_tasks[i + 1].get("due_date")
