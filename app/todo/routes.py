from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.auth.auth_bearer import JWTBearer
from app.todo.schemas import CreateTodo, TodoResponse, UpdateTodo
from app.todo.services import TodoService
from config import get_session

router = APIRouter(prefix="/api/todo", tags=["Todo"])

@router.get("/", dependencies=[Depends(JWTBearer())], response_model=list[TodoResponse])
def get_all_todos(session: Session = Depends(get_session)):
    """Get all todos."""
    service = TodoService(session)
    return service.get_all_todos()

@router.post("/create/", dependencies=[Depends(JWTBearer())], response_model=TodoResponse)
def create_todo(todo: CreateTodo, session: Session = Depends(get_session)):
    """Create a new todo and return its details."""
    service = TodoService(session)
    return service.create_todo(todo)

@router.get("/{email}/", dependencies=[Depends(JWTBearer())], response_model=list[TodoResponse])
def get_todo_by_email(email: str, session: Session = Depends(get_session)):
    """Get all todos associated with the given email."""
    service = TodoService(session)
    return service.get_todo_by_email(email)

@router.put("/{todo_id}/", dependencies=[Depends(JWTBearer())], response_model=TodoResponse)
def update_todo(todo_id: int, todo: UpdateTodo, session: Session = Depends(get_session)):
    """Update an existing todo and return its details."""
    service = TodoService(session)
    return service.update_todo(todo_id, todo)

@router.delete("/{todo_id}/", dependencies=[Depends(JWTBearer())])
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    """Delete a todo by its ID."""
    service = TodoService(session)
    service.delete_todo(todo_id)
    return {"message": f"Todo with ID {todo_id} deleted successfully"}