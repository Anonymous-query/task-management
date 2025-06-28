from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...schemas.user import UserCreate, UserResponse, UserLogin, Token
from ...services.auth_service import auth_service
from ...services.user_service import user_service

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    return user_service.create_user(db=db, user=user)


@router.post("/login", response_model=Token)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """Login and get access token"""
    return auth_service.login(db=db, login_data=login_data)