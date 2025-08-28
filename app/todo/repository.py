from sqlmodel import Session, select
from typing import List, Optional

from app.todo.models import TodoBase

class TodoRepository:
    def __init__(self, session: Session):
        """Initialize repository with a database session."""
        self.session = session

    def get_all_todos(self) -> List[TodoBase]:
        """Fetch all todos from the database."""
        statement = select(TodoBase)
        return self.session.exec(statement).all()
    
    def create_todo(self, todo: TodoBase) -> TodoBase:
        """Create a new todo in the database and return it."""
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def get_todo_by_email(self, email: str) -> List[TodoBase]:
        """Retrieve all todos associated with the given email."""
        statement = select(TodoBase).where(TodoBase.email == email)
        return self.session.exec(statement).all()
    
    def get_todo_by_id(self, todo_id: int) -> Optional[TodoBase]:
        """Retrieve a todo by its ID."""
        statement = select(TodoBase).where(TodoBase.id == todo_id)
        return self.session.exec(statement).one_or_none()
    
    def update_todo(self, todo: TodoBase) -> TodoBase:
        """Update an existing todo in the database."""
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo
    
    def delete_todo(self, todo: TodoBase) -> None:
        """Delete a todo from the database."""
        self.session.delete(todo)
        self.session.commit()