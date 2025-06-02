from sqlmodel import Session, select
from app.users.models import UserBase
from typing import List, Optional

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: UserBase) -> UserBase:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> Optional[UserBase]:
        statement = select(UserBase).where(UserBase.email == email)
        return self.session.exec(statement).first()

    def get_all_users(self) -> List[UserBase]:
        statement = select(UserBase)
        return self.session.exec(statement).all()

    def update_user(self, user: UserBase) -> UserBase:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user