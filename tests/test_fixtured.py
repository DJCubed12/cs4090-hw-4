import pytest

from ..src.tasks import filter_tasks_by_completion, search_tasks


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


def test_filter_by_completion_completed(tasks):
    completed = filter_tasks_by_completion(tasks, True)
    assert all(t.get("completed") == True for t in completed)


def test_filter_by_completion_uncompleted(tasks):
    completed = filter_tasks_by_completion(tasks, False)
    assert all(t.get("completed") == False for t in completed)


def test_search_tasks_by_title(tasks):
    results = search_tasks(tasks, "Second")
    assert all("Second" in t.get("title") for t in results)


def test_search_tasks_by_description(tasks):
    results = search_tasks(tasks, "last")
    assert all("last" in t.get("description") for t in results)


def test_search_tasks_no_results(tasks):
    results = search_tasks(tasks, "dinosaurs")
    assert len(results) == 0
