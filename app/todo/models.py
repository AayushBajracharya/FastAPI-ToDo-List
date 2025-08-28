from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum

class Status(str, Enum):
    IN_PROGRESS = "in-progress"
    PENDING = "pending"
    COMPLETED = "completed"

class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"

class TodoBase(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    status: Status = Field(default=Status.PENDING)
    due_date: Optional[datetime] = Field(default=None)
    priority: Priority = Field(default=Priority.NONE)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    email: str = Field(foreign_key="userbase.email")