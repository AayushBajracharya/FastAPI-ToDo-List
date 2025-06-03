from app.auth.hashing import hash_password, verify_password
from app.users.models import UserBase
from app.auth.repository import AuthRepository
from app.auth.schemas import UserCreate, UserLogin
from fastapi import HTTPException, status

class AuthService:
    def __init__(self, session):
        """Initialize service with a database session."""
        self.repository = AuthRepository(session)

    def register_user(self, user_data: UserCreate) -> UserBase:
        """Register a new user with hashed password."""
        existing_user = self.repository.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        hashed_password = hash_password(user_data.password)
        db_user = UserBase(
            **user_data.model_dump(exclude={"password"}),
            password=hashed_password
        )
        return self.repository.create_user(db_user)

    def login_user(self, user_data: UserLogin) -> UserBase:
        """Validate user credentials and return user object."""
        user = self.repository.get_user_by_email(user_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email"
            )
        if not verify_password(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
            )
        return user
        