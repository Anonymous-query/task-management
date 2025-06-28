from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..core.security import security
from ..models.user import User
from ..schemas.user import UserLogin, Token, UserResponse
from .user_service import user_service

class AuthService:
    def authenticate_user(self, db: Session, login_data: UserLogin) -> Optional[User]:
        # Try to get user by username first, then by email
        user = user_service.get_user_by_username(db, login_data.username_or_email)
        if not user:
            user = user_service.get_user_by_email(db, login_data.username_or_email)
        
        if not user or not security.verify_password(login_data.password, user.hashed_password):
            return None
        
        return user
    
    def login(self, db: Session, login_data: UserLogin) -> Token:
        user = self.authenticate_user(db, login_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username/email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        access_token = security.create_access_token(
            data={"sub": user.username}
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(user)
        )
    
auth_service = AuthService()