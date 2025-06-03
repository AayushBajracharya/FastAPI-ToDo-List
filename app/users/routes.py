from fastapi import APIRouter, Depends
from app.users.schemas import UserCreate, UserLogin, UserResponse
from app.users.services import UserService
from config import get_session
from sqlmodel import Session
from typing import List

router = APIRouter(prefix="/api", tags=["AUTH"])

@router.post("/auth/register/", response_model=UserResponse)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    service = UserService(session)
    return service.register_user(user)

@router.post("/auth/login/")
def login_user(user: UserLogin, session: Session = Depends(get_session)):
    service = UserService(session)
    return service.login_user(user)

@router.get("/users/", response_model=List[UserResponse])
def get_all_users(session: Session = Depends(get_session)):
    service = UserService(session)
    return service.get_all_users()

@router.get("/users/{email}/", response_model=UserResponse)
def get_user_by_email(email: str, session: Session = Depends(get_session)):
    service = UserService(session)
    return service.get_user_by_email(email)
