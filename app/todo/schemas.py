from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.todo.models import Priority, Status


class CreateTodo(BaseModel):
    title: str
    description: Optional[str] = None
    status: Status = Status.PENDING
    due_date: Optional[datetime] = None
    priority: Priority = Priority.NONE
    email: EmailStr

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Status = Status.PENDING
    due_date: Optional[datetime] = None
    priority: Priority = Priority.NONE
    created_at: datetime
    updated_at: Optional[datetime] = None
    email: EmailStr

class UpdateTodo(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    due_date: Optional[datetime] = None
    priority: Optional[Priority] = None