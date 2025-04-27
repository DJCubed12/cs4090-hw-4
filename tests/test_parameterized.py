import pytest

from ..src.tasks import filter_tasks_by_priority, filter_tasks_by_category


@pytest.mark.parametrize("priority", ["Low", "Medium", "High"])
def test_filter_by_priority(priority):
    tasks = [
        {"id": 0, "priority": "Low"},
        {"id": 1, "priority": "High"},
        {"id": 2, "priority": "Medium"},
    ]

    filtered = filter_tasks_by_priority(tasks, priority)

    assert all(t.get("priority") == priority for t in filtered)


@pytest.mark.parametrize("category", ["Work", "School", "Personal", "Other"])
def test_filter_by_category(category):
    tasks = [
        {"id": 0, "category": "Other"},
        {"id": 1, "category": "Work"},
        {"id": 2, "category": "School"},
        {"id": 3, "category": "Personal"},
    ]

    filtered = filter_tasks_by_category(tasks, category)

    assert all(t.get("category") == category for t in filtered)
