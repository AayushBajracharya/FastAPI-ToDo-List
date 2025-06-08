from app.users.models import UserBase
from app.users.repository import UserRepository
from fastapi import HTTPException, status

class UserService:
    def __init__(self, session):
        self.repository = UserRepository(session)

    def get_all_users(self) -> list[UserBase]:
        return self.repository.get_all_users()

    def get_user_by_email(self, email: str) -> UserBase:
        user = self.repository.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    