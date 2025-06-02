from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class UserBase(SQLModel, table=True):
    email: str = Field(primary_key=True)
    username: str = Field(max_length=100, index=True)
    password: str = Field(min_length=8)
    updatedAt: Optional[datetime] = Field(default_factory=datetime.now)
    createdAt: datetime = Field(default_factory=datetime.now)