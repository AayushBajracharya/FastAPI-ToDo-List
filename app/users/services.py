from app.users.models import UserBase
from app.users.schemas import UserCreate, UserLogin
from app.users.repository import UserRepository
from app.users.hashing import hash_password, verify_password
from datetime import datetime
from fastapi import HTTPException, status

class UserService:
    def __init__(self, session):
        self.repository = UserRepository(session)

    def register_user(self, user_data: UserCreate) -> UserBase:
        # Check if email already exists
        existing_user = self.repository.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        # Create new user with hashed password
        hashed_password = hash_password(user_data.password)
        db_user = UserBase(
            email=user_data.email,
            username=user_data.username,
            password=hashed_password,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        return self.repository.create_user(db_user)

    def login_user(self, user_data: UserLogin) -> str:
        user = self.repository.get_user_by_email(user_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        if not verify_password(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        return "Login successful"

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