from datetime import datetime
from fastapi import HTTPException, status
from app.todo.models import TodoBase
from app.todo.repository import TodoRepository
from app.todo.schemas import CreateTodo, UpdateTodo
from pydantic import EmailStr

class TodoService:
    def __init__(self, session):
        """Initialize service with a database session."""
        self.repository = TodoRepository(session)

    def get_all_todos(self) -> list[TodoBase]:
        """Get all todos with error handling."""
        try:
            todos = self.repository.get_all_todos()
            if not todos:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No todos found"
                )
            return todos
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch todos: {str(e)}"
            )

    def create_todo(self, todo_data: CreateTodo) -> TodoBase:
        """Create a new todo with error handling."""
        try:
            db_todo = TodoBase(**todo_data.model_dump())
            return self.repository.create_todo(db_todo)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create todo: {str(e)}"
            )

    def get_todo_by_email(self, email: EmailStr) -> list[TodoBase]:
        """Retrieve all todos for a given email with error handling."""
        try:
            todos = self.repository.get_todo_by_email(email)
            if not todos:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No todos found for email: {email}"
                )
            return todos
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch todos for email {email}: {str(e)}"
            )

    def update_todo(self, todo_id: int, todo_data: UpdateTodo) -> TodoBase:
        """Update an existing todo with error handling."""
        try:
            db_todo = self.repository.get_todo_by_id(todo_id)
            if not db_todo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Todo with ID {todo_id} not found"
                )
            for key, value in todo_data.model_dump(exclude_unset=True).items():
                setattr(db_todo, key, value)
            db_todo.updated_at = datetime.now()
            return self.repository.update_todo(db_todo)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update todo with ID {todo_id}: {str(e)}"
            )
        
    def delete_todo(self, todo_id: int) -> None:
        """Delete a todo with error handling."""
        try:
            db_todo = self.repository.get_todo_by_id(todo_id)
            if not db_todo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Todo with ID {todo_id} not found"
                )
            self.repository.delete_todo(db_todo)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete todo with ID {todo_id}: {str(e)}"
            )