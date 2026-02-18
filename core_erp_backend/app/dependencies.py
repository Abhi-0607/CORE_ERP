from typing import List, Optional
from app.models.users import User
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import crud, models
from app.core.config import settings
from app.database import get_db
from app.utils.permissions import Permission
from app.constants.roles import UserRole
from app.core.security import bearer_scheme

def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> User:
    token = None

    # 1) Authorization header
    if credentials:
        token = credentials.credentials

    # 2) Cookie
    if not token:
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def require_roles(required_roles: List[UserRole]):
    def role_checker(current_user: User = Depends(get_current_user)):
        user_role = current_user.role

        # normalize user_role into string
        if hasattr(user_role, "value"):
            user_role = user_role.value

        allowed = [
            r.value if hasattr(r, "value") else r
            for r in required_roles
        ]

        if user_role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user

    return role_checker

def get_current_active_user(current_user: models.users.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user