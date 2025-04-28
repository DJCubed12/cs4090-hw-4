from hypothesis import given, strategies as st

from datetime import datetime, timedelta

from ..src.tasks import (
    generate_unique_id,
    extend_task_due_date,
    filter_tasks_by_completion,
    get_overdue_tasks,
)


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


@given(st.lists(st.booleans(), max_size=1000))
def test_filter_tasks_by_completion(bools: list[bool]):
    num_completed = bools.count(True)
    tasks = [{"id": id, "completed": c} for id, c in enumerate(bools)]

    completed = filter_tasks_by_completion(tasks)

    assert len(completed) == num_completed
    assert all(t["completed"] == True for t in completed)


@given(
    years=st.lists(st.integers(-15, 15), min_size=20, max_size=20),
    months=st.lists(st.integers(1, 12), min_size=20, max_size=20),
    days=st.lists(st.integers(1, 28), min_size=20, max_size=20),
    completed_bools=st.lists(st.booleans(), min_size=20, max_size=20),
)
def test_get_overdue_tasks(years, months, days, completed_bools):
    now = datetime.now()
    num_overdue = 0
    tasks = []
    for i in range(len(years)):
        due_date = datetime(now.year + years[i], months[i], days[i])
        completed = completed_bools[i]
        tasks.append(
            {"id": i, "due_date": due_date.strftime("%Y-%m-%d"), "completed": completed}
        )

        if not completed and due_date < now:
            num_overdue += 1

    overdue_tasks = get_overdue_tasks(tasks)

    assert len(overdue_tasks) == num_overdue
    assert all(t.get("due_date") < now.strftime("%Y-%m-%d") for t in overdue_tasks)
