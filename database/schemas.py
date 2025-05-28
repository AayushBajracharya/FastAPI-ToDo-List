from .models import Todo

def individual_data(todo: Todo):
    return {
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "status": todo.is_completed,
    }

def all_tasks(todos: list[Todo]):
    return [individual_data(todo) for todo in todos]
