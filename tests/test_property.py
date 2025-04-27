from hypothesis import given, strategies as st

from datetime import datetime, timedelta

from ..src.tasks import generate_unique_id, extend_task_due_date


@given(st.lists(st.integers(1), unique=True))
def test_generate_unique_id(existing_ids):
    tasks = [{"id": id} for id in existing_ids]

    new_id = generate_unique_id(tasks)

    assert new_id not in existing_ids


@given(
    y=st.integers(2000, 2025),
    m=st.integers(1, 12),
    d=st.integers(1, 28),
    extension=st.integers(0, 1000),
)
def test_extend_task_due_date(y, m, d, extension):
    original_date = datetime(y, m, d)
    task = {"id": 1, "due_date": original_date.strftime("%Y-%m-%d")}

    extend_task_due_date(task, extension)

    expected_date = original_date + timedelta(extension)
    assert task.get("due_date") == expected_date.strftime("%Y-%m-%d")
