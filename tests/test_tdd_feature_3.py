import pytest

from ..src.tasks import get_first_n


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


@pytest.mark.parametrize("n", [0, 1, 2, 3])
def test_get_first_n_always_short(tasks, n):
    short_list = get_first_n(tasks, n)
    assert len(short_list) == n


@pytest.mark.parametrize("n", [4, 5, 6])
def test_get_first_n_same_or_longer(tasks, n):
    original_len = len(tasks)
    short_list = get_first_n(tasks, n)
    assert len(short_list) == original_len
