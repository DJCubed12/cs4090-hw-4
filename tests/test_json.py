import pytest

import os

from ..src.tasks import load_tasks, save_tasks


def test_load_tasks_success():
    """Expects to be run in the root of the project (one level above tests folder)."""
    tasks = load_tasks("tests/sample_data/tasks.json")
    assert len(tasks) == 3


def test_load_tasks_file_not_found():
    tasks = load_tasks("this_is_not_a_file.json")
    assert tasks == []


def test_load_tasks_invalid_json():
    """Expects to be run in the root of the project (one level above tests folder)."""
    tasks = load_tasks("tests/sample_data/bad_json.json")
    assert tasks == []


def test_load_and_save():
    """Expects to be run in the root of the project (one level above tests folder)."""
    loaded_tasks = load_tasks("tests/sample_data/tasks.json")
    save_tasks(loaded_tasks, "tests/save_tasks_test_output.json")

    assert os.path.exists("tests/save_tasks_test_output.json")

    with open("tests/sample_data/tasks.json", "r") as original_file:
        original_file_contents = original_file.read()
    with open("tests/save_tasks_test_output.json", "r") as saved_file:
        saved_file_contents = saved_file.read()

    assert original_file_contents == saved_file_contents

    os.remove("tests/save_tasks_test_output.json")
