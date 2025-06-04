from typing import Optional
from sqlmodel import Session, select
from app.users.models import UserBase
class AuthRepository:
    def __init__(self, session: Session):
        """Initialize repository with a database session."""
        self.session = session

    def create_user(self, user: UserBase) -> UserBase:
        """Create a new user in the database and return it."""
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> Optional[UserBase]:
        """Retrieve a user by email or return None if not found."""
        statement = select(UserBase).where(UserBase.email == email)
        return self.session.exec(statement).first()
    
    def update_user(self, user: UserBase) -> UserBase:
        """Update an existing user in the database and return it."""
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    