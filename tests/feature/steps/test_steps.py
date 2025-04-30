import pytest
from pytest_bdd import given, when, then, scenarios, parsers

import sys
import os
from datetime import datetime, timedelta

from ....src.tasks import (
    generate_unique_id,
    save_tasks,
    filter_tasks_by_priority,
    filter_tasks_by_category,
    get_overdue_tasks,
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Link the feature files
scenarios(
    "../generate_id.feature",
    "../save_tasks.feature",
    "../filter_by_priority.feature",
    "../filter_by_category.feature",
    "../get_overdue_tasks.feature",
)


@pytest.fixture
def context():
    return {"tasks": None}


@given("I have a list of tasks")
@given("I have a list of overdue tasks")
def step_make_task_list(context):
    context["tasks"] = (
        {
            "id": 1,
            "title": "First",
            "description": "first desc",
            "priority": "Low",
            "category": "Work",
            "due_date": "2025-02-10",
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
            "title": "Other",
            "description": "",
            "priority": "High",
            "category": "School",
            "due_date": "2025-02-10",
            "completed": True,
            "created_at": "2025-01-10 17:54:16",
        },
    )


@given("I have a list of not-yet-due tasks")
def step_make_task_list(context):
    context["tasks"] = (
        {
            "id": 1,
            "title": "First",
            "description": "first desc",
            "priority": "Low",
            "category": "Work",
            "due_date": (datetime.now() + timedelta(1)).strftime("%Y-%m-%d"),
            "completed": False,
            "created_at": "2025-01-10 17:54:10",
        },
        {
            "id": 2,
            "title": "Second",
            "description": "description",
            "priority": "Medium",
            "category": "Personal",
            "due_date": (datetime.now() + timedelta(2)).strftime("%Y-%m-%d"),
            "completed": True,
            "created_at": "2025-01-10 17:54:16",
        },
    )


@given("there are no tasks")
def step_no_tasks(context):
    context["tasks"] = []


@when("I generate a new ID")
def step_generate_unique_id(context):
    context["new_id"] = generate_unique_id(context["tasks"])


@when("I save the tasks")
def step_save_tasks(context):
    save_tasks(context["tasks"], "save_tasks_test_output.json")
    context["save_file"] = "save_tasks_test_output.json"


@when(parsers.parse("I filter by {priority} priority"))
def step_filter_for_priority(context, priority: str):
    context["filtered_tasks"] = filter_tasks_by_priority(context["tasks"], priority)


@when(parsers.parse("I filter by {category} category"))
def step_filter_for_priority(context, category: str):
    context["filtered_tasks"] = filter_tasks_by_category(context["tasks"], category)


@when("I get all overdue tasks")
def step_filter_for_priority(context):
    context["filtered_tasks"] = get_overdue_tasks(context["tasks"])


@then("the new ID is unique")
def step_then_id_is_unique(context):
    id = context["new_id"]
    assert id not in [task["id"] for task in context["tasks"]]


@then("the new ID is 1")
def step_id_is_1(context):
    assert context["new_id"] == 1


@then("the saved file exists")
def step_check_for_saved_file(context):
    assert os.path.exists(context["save_file"])


@then(parsers.parse("only tasks with {priority} priority are left"))
def step_check_filtered_task_priorities(context, priority: str):
    for task in context["filtered_tasks"]:
        assert task["priority"] == priority


@then(parsers.parse("only tasks with {category} category are left"))
def step_check_filtered_task_categories(context, category: str):
    for task in context["filtered_tasks"]:
        assert task["category"] == category


@then("I have all tasks from the original list")
def step_check_all_exist(context):
    original_task_ids = [task["id"] for task in context["tasks"]]
    for task in context["filtered_tasks"]:
        assert task["id"] in original_task_ids


@then("I have no tasks")
def step_check_for_empty(context):
    assert context["filtered_tasks"] == []
