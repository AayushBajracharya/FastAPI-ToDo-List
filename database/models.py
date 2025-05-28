from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    is_completed: bool = False
    is_deleted: bool = False
    updated_at: int = int(datetime.timestamp(datetime.now()))
    creation: int = int(datetime.timestamp(datetime.now()))
