import pytest

import os

from ..src.tasks import load_tasks, save_tasks


test_dir = os.path.dirname(__file__)


def test_load_tasks_success():
    """Expects to be run in the root of the project (one level above tests folder)."""
    json_file = os.path.join(test_dir, "sample_data", "tasks.json")
    tasks = load_tasks(json_file)
    assert len(tasks) == 3


def test_load_tasks_file_not_found():
    tasks = load_tasks("this_is_not_a_file.json")
    assert tasks == []


def test_load_tasks_invalid_json():
    """Expects to be run in the root of the project (one level above tests folder)."""
    bad_json_file = os.path.join(test_dir, "sample_data", "bad_json.json")
    tasks = load_tasks(bad_json_file)
    assert tasks == []


def test_load_and_save():
    """Expects to be run in the root of the project (one level above tests folder)."""
    json_file_path = os.path.join(test_dir, "sample_data", "tasks.json")
    loaded_tasks = load_tasks(json_file_path)

    save_file_path = os.path.join(test_dir, "save_tasks_test_output.json")
    save_tasks(loaded_tasks, save_file_path)

    assert os.path.exists(save_file_path)

    with open(json_file_path, "r") as original_file:
        original_file_contents = original_file.read()
    with open(save_file_path, "r") as saved_file:
        saved_file_contents = saved_file.read()

    assert original_file_contents == saved_file_contents

    os.remove(save_file_path)
