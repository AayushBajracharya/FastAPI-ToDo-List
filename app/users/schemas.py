from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserResponse(BaseModel):
    email: EmailStr
    username: str
    createdAt: datetime
    updatedAt: Optional[datetime]
