from fastapi import APIRouter, Depends
from app.auth.auth_bearer import JWTBearer
from app.users.schemas import UserResponse
from app.users.services import UserService
from config import get_session
from sqlmodel import Session
from typing import List

router = APIRouter(prefix="/api/user", tags=["User"])

@router.get("/",  dependencies=[Depends(JWTBearer())], response_model=List[UserResponse])
def get_all_users(session: Session = Depends(get_session)):
    service = UserService(session)
    return service.get_all_users()

@router.get("/users/{email}/", dependencies=[Depends(JWTBearer())], response_model=UserResponse)
def get_user_by_email(email: str, session: Session = Depends(get_session)):
    service = UserService(session)
    return service.get_user_by_email(email)
