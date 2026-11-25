To-Do List Application

A beginner-friendly Python to-do list with both a desktop GUI and a command-line version. Tasks are saved in a JSON file, so they are still available the next time you open the app.

## Features

- Add tasks
- View the task list
- Mark tasks as completed
- Delete tasks
- Save tasks between sessions in `tasks.json`

## Requirements

- Python 3
- Tkinter for the desktop GUI (usually included with Python)

No extra Python packages are required.

## Run the GUI

Open a terminal in this project folder and run:

```bash
python3 todo_gui.py
```

Type a task in the **New Task** box and choose **Add task**. Select a task in the list before choosing **Mark complete** or **Delete selected**.

## Run the command-line version

Run:

```bash
python3 todo.py
```

Choose an option from the menu and follow the prompts.

## Saved tasks

Both versions use the same `tasks.json` file in this project folder. The file is created automatically when you add your first task. You can keep using either version, and both will use the saved list.

