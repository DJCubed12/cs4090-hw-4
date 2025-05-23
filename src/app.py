import streamlit as st
from datetime import datetime

from tasks import (
    get_first_n,
    load_tasks,
    save_tasks,
    generate_unique_id,
    filter_tasks_by_priority,
    filter_tasks_by_category,
    extend_task_due_date,
    sort_by_due_date,
)

from run_tests import (
    run_basic_tests,
    run_bdd_tests,
    run_coverage_test,
    run_fixtured_tests,
    run_property_tests,
    run_tdd_tests,
    run_test_with_html_report,
    run_parameterized_tests,
)


def main():
    st.title("To-Do Application")

    # Load existing tasks
    tasks = load_tasks()

    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")

    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox(
            "Category", ["Work", "Personal", "School", "Other"]
        )
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")

        if submit_button and task_title:
            new_task = {
                "id": generate_unique_id(tasks),
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")

    # Main area to display tasks
    st.header("Your Tasks")

    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox(
            "Filter by Category",
            ["All"] + list(set([task["category"] for task in tasks])),
        )
        show_completed = st.checkbox("Show Completed Tasks")
    with col2:
        filter_priority = st.selectbox(
            "Filter by Priority", ["All", "High", "Medium", "Low"]
        )
        show_first_n = st.number_input("Only show n", -1)
        st.caption("Use -1 to show all")

    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]

    # Sort and truncate
    sorted_filtered_tasks = sort_by_due_date(filtered_tasks)
    if show_first_n >= 0:
        sorted_filtered_tasks = get_first_n(sorted_filtered_tasks, show_first_n)

    # Display tasks
    for task in sorted_filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task["description"])
            st.caption(
                f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}"
            )
        with col2:
            if st.button(
                "Complete" if not task["completed"] else "Undo",
                key=f"complete_{task['id']}",
            ):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()
            if st.button("Extend", key=f"extend_{task['id']}"):
                extend_task_due_date(task, 1)
                save_tasks(tasks)
                st.rerun()

    # Buttons to run tests
    st.header("Tests")

    if st.button("Basic tests"):
        with st.status("Running tests...") as status:
            exit_code = run_basic_tests()
            if exit_code:
                status.update(
                    label=f"Pytest exited with code {exit_code}", state="error"
                )
    if st.button("Parameterized tests"):
        with st.status("Running tests...") as status:
            exit_code = run_parameterized_tests()
            if exit_code:
                status.update(
                    label=f"Pytest exited with code {exit_code}", state="error"
                )
    if st.button("Tests with fixture"):
        with st.status("Running tests...") as status:
            exit_code = run_fixtured_tests()
            if exit_code:
                status.update(
                    label=f"Pytest exited with code {exit_code}", state="error"
                )
    if st.button("Coverage test"):
        with st.status("Running tests...") as status:
            exit_code = run_coverage_test()
            if exit_code:
                status.update(
                    label=f"Pytest exited with code {exit_code}. Coverage statistics saved at src/.coverage",
                    state="error",
                )
            else:
                status.update(
                    label="Coverage statistics saved at src/.coverage", state="complete"
                )
    if st.button("Get HTML test report"):
        with st.status("Running tests...") as status:
            report_path = run_test_with_html_report()
            status.update(label=f"HTML report saved to {report_path}")
    if st.button("TDD tests"):
        with st.status("Running tests...") as status:
            exit_code = run_tdd_tests()
            if exit_code:
                status.update(
                    label=f"Pytest exited with code {exit_code}", state="error"
                )
    if st.button("BDD tests"):
        with st.status("Running tests...") as status:
            exit_code = run_bdd_tests()
            if exit_code:
                status.update(
                    label=f"Pytest exited with code {exit_code}", state="error"
                )
    if st.button("Property tests"):
        with st.status("Running tests...") as status:
            exit_code = run_property_tests()
            if exit_code:
                status.update(
                    label=f"Pytest exited with code {exit_code}", state="error"
                )


if __name__ == "__main__":
    main()
