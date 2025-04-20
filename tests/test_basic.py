import pytest

from ..src.tasks import (
    filter_tasks_by_category,
    filter_tasks_by_completion,
    generate_unique_id,
    filter_tasks_by_priority,
)


def test_generate_unique_id_empty():
    assert generate_unique_id([]), 1


def test_generate_unique_id_not_empty():
    tasks = [{"id": 0}, {"id": 2}, {"id": 1}]
    assert generate_unique_id(tasks), 3


def test_filter_tasks_by_priority():
    tasks = [
        {"id": 0, "priority": "Low"},
        {"id": 1, "priority": "High"},
        {"id": 2, "priority": "Medium"},
    ]

    low_priority = filter_tasks_by_priority(tasks, "Low")
    assert len(low_priority) == 1
    assert all(t["priority"] == "Low" for t in low_priority)

    med_priority = filter_tasks_by_priority(tasks, "Medium")
    assert len(med_priority) == 1
    assert all(t["priority"] == "Medium" for t in med_priority)

    high_priority = filter_tasks_by_priority(tasks, "High")
    assert len(high_priority) == 1
    assert all(t["priority"] == "High" for t in high_priority)


def test_filter_tasks_by_category():
    tasks = [
        {"id": 0, "category": "Other"},
        {"id": 1, "category": "Work"},
        {"id": 2, "category": "School"},
        {"id": 3, "category": "Personal"},
    ]

    other = filter_tasks_by_category(tasks, "Other")
    assert len(other) == 1
    assert all(t["category"] == "Other" for t in other)

    work = filter_tasks_by_category(tasks, "Work")
    assert len(work) == 1
    assert all(t["category"] == "Work" for t in work)

    school = filter_tasks_by_category(tasks, "School")
    assert len(school) == 1
    assert all(t["category"] == "School" for t in school)

    personal = filter_tasks_by_category(tasks, "Personal")
    assert len(personal) == 1
    assert all(t["category"] == "Personal" for t in personal)


def test_filter_tasks_by_completion():
    tasks = [
        {"id": 0, "completed": False},
        {"id": 1, "completed": True},
        {"id": 2, "completed": False},
        {"id": 3, "completed": True},
    ]

    completed = filter_tasks_by_completion(tasks, True)
    assert len(completed) == 2
    assert all(t["completed"] == True for t in completed)

    uncompleted = filter_tasks_by_completion(tasks, False)
    assert len(uncompleted) == 2
    assert all(t["completed"] == False for t in uncompleted)
