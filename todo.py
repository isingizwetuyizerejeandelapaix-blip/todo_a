import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "tasks.json"


def load_tasks():
    """Read tasks from the JSON file, or start with an empty list."""
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_tasks():
    """Write the current tasks to the JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


tasks = load_tasks()


def add_task():
    """Ask for a task and add it to the list."""
    title = input("Enter a new task: ").strip()
    if not title:
        print("A task cannot be empty.")
        return

    tasks.append({"title": title, "completed": False})
    save_tasks()
    print("Task added.")


def show_tasks():
    """Print all tasks, or a message when the list is empty."""
    if not tasks:
        print("No tasks yet.")
        return

    print("Your tasks:")
    for number, task in enumerate(tasks, start=1):
        if task["completed"]:
            status = "done"
        else:
            status = "not done"
        print(f"{number}. {task['title']} ({status})")


def delete_task():
    """Remove a task selected by its number."""
    if not tasks:
        print("There are no tasks to delete.")
        return

    show_tasks()
    answer = input("Enter the number of the task to delete: ").strip()

    try:
        number = int(answer)
    except ValueError:
        print("Please enter a task number.")
        return

    if number < 1 or number > len(tasks):
        print("No task has that number.")
        return

    deleted_task = tasks.pop(number - 1)
    save_tasks()
    print(f"Deleted: {deleted_task['title']}")


def complete_task():
    """Mark a task selected by its number as completed."""
    if not tasks:
        print("There are no tasks to mark as completed.")
        return

    show_tasks()
    answer = input("Enter the number of the completed task: ").strip()

    try:
        number = int(answer)
    except ValueError:
        print("Please enter a task number.")
        return

    if number < 1 or number > len(tasks):
        print("No task has that number.")
        return

    task = tasks[number - 1]
    task["completed"] = True
    save_tasks()
    print(f"Marked as done: {task['title']}")


def main():
    """Show the menu and run the selected action."""
    while True:
        print("\nTo-Do List")
        print("1. View tasks")
        print("2. Add a task")
        print("3. Delete a task")
        print("4. Mark a task as completed")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            show_tasks()
        elif choice == "2":
            add_task()
            show_tasks()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            complete_task()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Please choose 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()
