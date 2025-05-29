from typing import List
from .models import Todo, TodoRead

def individual_data(todo: Todo) -> TodoRead:
    return TodoRead(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        is_completed=todo.is_completed,
        is_deleted=todo.is_deleted,
        updated_at=todo.updated_at,
        creation=todo.creation
    )

def all_tasks(todos: List[Todo]) -> List[TodoRead]:
    return [individual_data(todo) for todo in todos]