import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox


DATA_FILE = Path(__file__).resolve().parent / "tasks.json"
BACKGROUND = "#F3F5F9"
CARD = "#FFFFFF"
TEXT = "#1D2738"
MUTED = "#748096"
BLUE = "#76C15A"
GREEN = "#168564"
BUTTON = "#111111"
BUTTON_ACTIVE = "#333333"


def load_tasks():
    """Load saved tasks, or start with an empty list."""
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        messagebox.showwarning(
            "Could not read tasks",
            "The tasks.json file is not valid JSON. The list will start empty.",
            parent=root,
        )
        return []


def save_tasks():
    """Save the current task list as JSON."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except OSError as error:
        messagebox.showerror(
            "Could not save tasks",
            f"The task list could not be saved.\n\n{error}",
            parent=root,
        )
        return False
    return True


def update_status(message):
    status_label.config(text=message)


def make_black_button(parent, text, command):
    """Create a clickable label so macOS keeps the chosen button colors."""
    button = tk.Label(
        parent,
        text=text,
        bg=BUTTON,
        fg="white",
        activebackground=BUTTON_ACTIVE,
        font=("Arial", 10, "bold"),
        padx=15,
        pady=10,
        cursor="hand2",
        takefocus=True,
    )
    button.bind("<Button-1>", lambda event: command())
    button.bind("<Enter>", lambda event: button.config(bg=BUTTON_ACTIVE))
    button.bind("<Leave>", lambda event: button.config(bg=BUTTON))
    button.bind("<Return>", lambda event: command())
    button.bind("<space>", lambda event: command())
    return button


def refresh_task_list():
    """Show saved tasks and update the list summary."""
    task_list.delete(0, tk.END)

    if not tasks:
        task_list.insert(tk.END, "No tasks yet — add one above.")
        task_list.itemconfig(0, foreground=MUTED)
    else:
        for index, task in enumerate(tasks):
            if task["completed"]:
                marker = "✓"
                color = GREEN
            else:
                marker = "○"
                color = TEXT
            task_list.insert(tk.END, f"{marker}   {task['title']}")
            task_list.itemconfig(index, foreground=color)

    remaining = sum(not task["completed"] for task in tasks)
    task_count = len(tasks)
    task_word = "task" if task_count == 1 else "tasks"
    summary_label.config(text=f"{task_count} {task_word} · {remaining} remaining")


def add_task():
    """Add a task from the text box."""
    title = task_entry.get().strip()
    if not title:
        messagebox.showwarning(
            "Task needed", "Type a task before choosing Add task.", parent=root
        )
        return

    tasks.append({"title": title, "completed": False})
    if not save_tasks():
        tasks.pop()
        return

    task_entry.delete(0, tk.END)
    refresh_task_list()
    update_status(f"Added: {title}")


def selected_task_index(action):
    """Return the selected task number, or show a helpful message."""
    if not tasks:
        messagebox.showinfo("No tasks", "Add a task to your list first.", parent=root)
        return None

    selection = task_list.curselection()
    if not selection:
        messagebox.showwarning(
            "Select a task", f"Choose a task before you {action} it.", parent=root
        )
        return None
    return selection[0]


def complete_task():
    """Mark the selected task as completed."""
    index = selected_task_index("mark")
    if index is None:
        return

    task = tasks[index]
    if task["completed"]:
        messagebox.showinfo("Already complete", "That task is already done.", parent=root)
        return

    task["completed"] = True
    if not save_tasks():
        task["completed"] = False
        return

    refresh_task_list()
    task_list.selection_set(index)
    update_status(f"Completed: {task['title']}")


def delete_task():
    """Delete the selected task."""
    index = selected_task_index("delete")
    if index is None:
        return

    deleted_task = tasks.pop(index)
    if not save_tasks():
        tasks.insert(index, deleted_task)
        return

    refresh_task_list()
    update_status(f"Deleted: {deleted_task['title']}")


root = tk.Tk()
root.title("My To-Do List")
root.geometry("700x600")
root.minsize(580, 520)
root.configure(bg=BACKGROUND)

tasks = load_tasks()

main_frame = tk.Frame(root, bg=BACKGROUND, padx=34, pady=28)
main_frame.pack(fill="both", expand=True)

tk.Label(
    main_frame,
    text="MY TASKS",
    bg=BACKGROUND,
    fg=BLUE,
    font=("Arial", 10, "bold"),
).pack(anchor="w")

tk.Label(
    main_frame,
    text="Make room for what matters.",
    bg=BACKGROUND,
    fg=TEXT,
    font=("Arial", 24, "bold"),
).pack(anchor="w", pady=(5, 3))

tk.Label(
    main_frame,
    text="Add a task, then select it to update your list.",
    bg=BACKGROUND,
    fg=MUTED,
    font=("Arial", 11),
).pack(anchor="w")

add_card = tk.Frame(main_frame, bg=CARD, padx=18, pady=16)
add_card.pack(fill="x", pady=(22, 14))

tk.Label(
    add_card,
    text="NEW TASK",
    bg=CARD,
    fg=MUTED,
    font=("Arial", 9, "bold"),
).pack(anchor="w", pady=(0, 9))

entry_row = tk.Frame(add_card, bg=CARD)
entry_row.pack(fill="x")

task_entry = tk.Entry(
    entry_row,
    font=("Arial", 12),
    bg="#FFFFFF",
    fg=TEXT,
    insertbackground=TEXT,
    selectbackground=BLUE,
    selectforeground="#FFFFFF",
    relief="solid",
    bd=1,
    highlightthickness=0,
)
task_entry.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 10))

add_button = make_black_button(entry_row, "Add task", add_task)
add_button.pack(side="right")
task_entry.bind("<Return>", lambda event: add_task())

list_card = tk.Frame(main_frame, bg=CARD, padx=18, pady=16)
list_card.pack(fill="both", expand=True)

list_header = tk.Frame(list_card, bg=CARD)
list_header.pack(fill="x", pady=(0, 10))

tk.Label(
    list_header,
    text="YOUR LIST",
    bg=CARD,
    fg=TEXT,
    font=("Arial", 10, "bold"),
).pack(side="left")

summary_label = tk.Label(
    list_header,
    text="",
    bg=CARD,
    fg=MUTED,
    font=("Arial", 10),
)
summary_label.pack(side="right")

list_area = tk.Frame(list_card, bg=CARD)
list_area.pack(fill="both", expand=True)

task_list = tk.Listbox(
    list_area,
    height=9,
    font=("Arial", 12),
    bg="#FAFBFD",
    fg=TEXT,
    selectbackground="#E1E8FF",
    selectforeground=TEXT,
    activestyle="none",
    relief="flat",
    bd=0,
    highlightthickness=0,
    selectmode=tk.SINGLE,
)
task_list.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(list_area, command=task_list.yview)
scrollbar.pack(side="right", fill="y")
task_list.config(yscrollcommand=scrollbar.set)

button_row = tk.Frame(list_card, bg=CARD)
button_row.pack(fill="x", pady=(13, 0))

make_black_button(button_row, "Mark complete", complete_task).pack(side="left")
make_black_button(button_row, "Delete selected", delete_task).pack(
    side="left", padx=(9, 0)
)

status_label = tk.Label(
    main_frame,
    text="Your list is saved automatically.",
    bg=BACKGROUND,
    fg=MUTED,
    font=("Arial", 9),
)
status_label.pack(anchor="w", pady=(12, 0))

refresh_task_list()
task_entry.focus_set()
root.mainloop()
