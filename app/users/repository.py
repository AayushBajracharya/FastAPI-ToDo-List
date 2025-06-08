from sqlmodel import Session, select
from app.users.models import UserBase
from typing import List, Optional

class UserRepository:
    def __init__(self, session: Session):
        """Initialize repository with a database session."""
        self.session = session

    def get_user_by_email(self, email: str) -> Optional[UserBase]:
        """Retrieve a user by email or return None if not found."""
        statement = select(UserBase).where(UserBase.email == email)
        return self.session.exec(statement).first()

    def get_all_users(self) -> List[UserBase]:
        """Fetch all users from the database."""
        statement = select(UserBase)
        return self.session.exec(statement).all()
