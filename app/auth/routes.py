from fastapi import APIRouter, Depends, HTTPException
from app.auth.hashing import create_access_token, create_refresh_token
from app.auth.schemas import PasswordResetConfirm, PasswordResetRequest, UserCreate, UserLogin, Token
from app.users.schemas import UserResponse
from app.auth.services import AuthService
from config import get_session
from sqlmodel import Session

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register/", response_model=UserResponse)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    """Register a new user and return user details."""
    service = AuthService(session)
    return service.register_user(user)

@router.post("/login/", response_model=Token)
def login_user(user: UserLogin, session: Session = Depends(get_session)):
    """Authenticate a user and return access and refresh tokens."""
    service = AuthService(session)
    service.login_user(user)
    access_token = create_access_token(subject=user.email)
    refresh_token = create_refresh_token(subject=user.email)
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/reset-password/request")
def request_password_reset(request: PasswordResetRequest, session: Session = Depends(get_session)):
    """Request a password reset OTP via email."""
    service = AuthService(session)
    return service.request_password_reset(request)

@router.post("/reset-password/confirm")
def confirm_password_reset(confirm: PasswordResetConfirm, session: Session = Depends(get_session)):
    """Confirm password reset with OTP and new password."""
    service = AuthService(session)
    return service.confirm_password_reset(confirm)
