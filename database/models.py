from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class TodoBase(SQLModel):
    title: str
    description: str
    is_completed: bool = False
    is_deleted: bool = False
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    creation: str = Field(default_factory=lambda: datetime.now().isoformat())

class Todo(TodoBase, table=True):
    id: int = Field(primary_key=True)

class TodoRead(TodoBase):
    id: int