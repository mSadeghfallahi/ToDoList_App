# To-Do List Application

A CLI-based To-Do list application with project and task management.

## Installation

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Create .env file:
```bash
cp .env.example .env
```

## Usage

Run the application:
```bash
poetry run todo
```

## Features

- Create, edit, and delete projects
- Create, edit, and delete tasks within projects
- List all projects and tasks
- Task status management (to-do, doing, done)
- Input validation
- Cascade deletion
