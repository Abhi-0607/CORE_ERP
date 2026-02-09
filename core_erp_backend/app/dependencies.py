from typing import List, Optional
from app.models.users import User
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import crud, models
from app.core.config import settings
from app.database import get_db
from app.utils.permissions import Permission
from app.constants.roles import UserRole
from app.core.security import bearer_scheme

async def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> models.users.User:
    
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.user.get(db, id=int(user_id))
    if user is None:
        raise credentials_exception
    
    print("PAYLOAD:", payload)
    print("crud:", dir(crud))

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