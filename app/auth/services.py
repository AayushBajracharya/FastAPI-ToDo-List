from datetime import datetime
from app.auth.hashing import hash_password, verify_password
from app.auth.otp import generate_otp, send_otp_email, store_otp, verify_otp
from app.users.models import UserBase
from app.auth.repository import AuthRepository
from app.auth.schemas import PasswordResetConfirm, PasswordResetRequest, UserCreate, UserLogin
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
        
    def request_password_reset(self, request: PasswordResetRequest) -> dict:
        """Generate and send OTP for password reset."""
        user = self.repository.get_user_by_email(request.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        otp = generate_otp()
        store_otp(request.email, otp)
        try:
            send_otp_email(request.email, otp)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to send OTP: {str(e)}"
            )
        return {"message": "OTP sent to email"}

    def confirm_password_reset(self, confirm: PasswordResetConfirm) -> dict:
        """Validate OTP and reset user password."""
        if not verify_otp(confirm.email, confirm.otp):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP"
            )
        user = self.repository.get_user_by_email(confirm.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        user.password = hash_password(confirm.new_password)
        user.updatedAt = datetime.now()
        self.repository.update_user(user)
        return {"message": "Password reset successful"}
    