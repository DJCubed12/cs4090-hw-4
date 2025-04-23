import pytest

import os
import datetime

from ..src.tasks import (
    filter_tasks_by_category,
    filter_tasks_by_completion,
    generate_unique_id,
    filter_tasks_by_priority,
    get_overdue_tasks,
    search_tasks,
    load_tasks,
    save_tasks,
)

TEST_DIR = os.path.dirname(__file__)


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


def test_search_tasks():
    tasks = [
        {"id": 0, "title": "Task0", "description": "description0"},
        {"id": 1, "title": "Task1", "description": "sample text"},
        {"id": 2, "title": "Coding", "description": "number 2"},
        {"id": 3, "title": "Task3", "description": "idk"},
    ]

    sample = search_tasks(tasks, "sample")
    assert len(sample) == 1
    assert sample[0]["id"] == 1

    coding = search_tasks(tasks, "Coding")
    assert len(coding) == 1
    assert coding[0]["id"] == 2

    anything_with_task = search_tasks(tasks, "Task")
    assert len(anything_with_task) == 3
    assert all(t["id"] != 2 for t in anything_with_task)

    assert len(search_tasks(tasks, "no_matches")) == 0


def test_get_overdue_tasks():
    tasks = [
        # Overdue
        {
            "id": 0,
            "completed": False,
            "due_date": datetime.datetime(2015, 1, 1).strftime("%Y-%m-%d"),
        },
        {
            "id": 1,
            "completed": False,
            "due_date": datetime.datetime(2025, 4, 10).strftime("%Y-%m-%d"),
        },
        # Old but completed
        {
            "id": 2,
            "completed": True,
            "due_date": datetime.datetime(2015, 1, 1).strftime("%Y-%m-%d"),
        },
        # Not completed, but in future
        {
            "id": 3,
            "completed": False,
            "due_date": datetime.datetime(3000, 1, 1).strftime("%Y-%m-%d"),
        },
        {
            "id": 4,
            "completed": False,
            "due_date": datetime.datetime(3300, 1, 1).strftime("%Y-%m-%d"),
        },
        # Completed not yet due
        {
            "id": 5,
            "completed": True,
            "due_date": datetime.datetime(3000, 1, 1).strftime("%Y-%m-%d"),
        },
    ]

    overdue = get_overdue_tasks(tasks)
    assert len(overdue) == 2
    assert tasks[0] in overdue
    assert tasks[1] in overdue


def test_load_tasks_success():
    """Expects to be run in the root of the project (one level above tests folder)."""
    json_file = os.path.join(TEST_DIR, "sample_data", "tasks.json")
    tasks = load_tasks(json_file)
    assert len(tasks) == 3


def test_load_tasks_file_not_found():
    tasks = load_tasks("this_is_not_a_file.json")
    assert tasks == []


def test_load_tasks_invalid_json():
    """Expects to be run in the root of the project (one level above tests folder)."""
    bad_json_file = os.path.join(TEST_DIR, "sample_data", "bad_json.json")
    tasks = load_tasks(bad_json_file)
    assert tasks == []


def test_load_and_save():
    """Expects to be run in the root of the project (one level above tests folder)."""
    json_file_path = os.path.join(TEST_DIR, "sample_data", "tasks.json")
    loaded_tasks = load_tasks(json_file_path)

    save_file_path = os.path.join(TEST_DIR, "save_tasks_test_output.json")
    save_tasks(loaded_tasks, save_file_path)

    assert os.path.exists(save_file_path)

    with open(json_file_path, "r") as original_file:
        original_file_contents = original_file.read()
    with open(save_file_path, "r") as saved_file:
        saved_file_contents = saved_file.read()

    assert original_file_contents == saved_file_contents

    os.remove(save_file_path)
