import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

# Create the tasks table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    due_date TEXT,
    completed INTEGER DEFAULT 0)
""")
conn.commit()


def add_task(description, due_date=None):
    """Add a task to the database."""
    cursor.execute(
        "INSERT INTO tasks (description, due_date) VALUES (?, ?)",
        (description, due_date)
    )
    conn.commit()
    print(f'Task "{description}" added.')


def view_tasks():
    """Display all tasks from the database."""
    cursor.execute("SELECT id, description, due_date, completed FROM tasks")
    rows = cursor.fetchall()
    if not rows:
        print("No tasks available.")
    else:
        print("Tasks:")
        for row in rows:
            task_id, description, due_date, completed = row
            status = "[x]" if completed else "[ ]"
            due = f" (Due: {due_date})" if due_date else ""
            print(f"{task_id}. {status} {description}{due}")


def edit_task(task_id, new_description=None, new_due_date=None):
    """Edit a task's description or due date."""
    if new_description:
        cursor.execute("UPDATE tasks SET description = ? WHERE id = ?",
                       (new_description, task_id))
    if new_due_date:
        cursor.execute("UPDATE tasks SET due_date = ? WHERE id = ?",
                       (new_due_date, task_id))
    if new_description or new_due_date:
        conn.commit()
        print("Task updated.")
    else:
        print("No changes made.")


def remove_task(task_id):
    """Remove a task from the database by its ID, with confirmation."""
    confirm = input(
        f"Are you sure you want to remove task {task_id}? (y/n): "
    ).strip().lower()
    if confirm != 'y':
        print("Task removal cancelled.")
        return
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    if cursor.rowcount == 0:
        print("Invalid task ID.")
    else:
        conn.commit()
        print(f"Task {task_id} removed.")


def mark_task_complete(task_id):
    """Mark a task as complete or incomplete based on user choice."""
    cursor.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        print("Invalid task ID.")
        return

    current_status = row[0]
    choice = input("Mark as (c)omplete or (i)ncomplete? ").strip().lower()

    if choice == 'c':
        if current_status == 1:
            print(f"Task {task_id} is already complete.")
        else:
            cursor.execute(
                "UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,)
            )
            conn.commit()
            print(f"Task {task_id} marked as complete.")
    elif choice == 'i':
        if current_status == 0:
            print(f"Task {task_id} is already incomplete.")
        else:
            cursor.execute("UPDATE tasks SET completed = 0 WHERE id = ?",
                           (task_id,))
            conn.commit()
            print(f"Task {task_id} marked as incomplete.")
    else:
        print("Invalid choice. Please enter 'c' or 'i'.")


def main():
    """Main function to run the task manager."""
    print("Welcome to the Task Manager!")
    input("Press Enter to continue...")

    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Edit Task")
        print("4. Remove Task")
        print("5. Mark Task Complete/Incomplete")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            description = input("Enter the task: ")
            due_date = input("Enter the due date (optional): ")
            add_task(description, due_date if due_date else None)

        elif choice == '2':
            view_tasks()

        elif choice == '3':
            try:
                task_id = int(input("Enter the task ID to edit: "))
                new_description = input(
                    "Enter the new description (leave blank to keep current): "
                )
                new_due_date = input(
                    "Enter the new due date (leave blank to keep current): "
                )
                edit_task(
                    task_id,
                    new_description if new_description else None,
                    new_due_date if new_due_date else None
                )
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '4':
            try:
                task_id = int(input("Enter the task ID to remove: "))
                remove_task(task_id)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '5':
            try:
                task_id = int(input(
                    "Enter task ID to mark complete/incomplete: "))
                mark_task_complete(task_id)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '6':
            print("\nExiting Task Manager.\n")
            print("Thank you for using the Task Manager!\n")
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()


if __name__ == "__main__":
    main()
