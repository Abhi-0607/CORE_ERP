from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database import get_db
from app.core.config import settings
from app.schemas.users import UserOut, Token, SignupRequest, LoginRequest
from app.utils.security import verify_password
from app.utils.token import create_access_token
from app.models.users import User
from app import crud
from app.core.security import bearer_scheme
from fastapi import Request, Response

router = APIRouter(prefix="/auth", tags=["Auth"])

# ----------------------------
# SIGNUP
# ----------------------------
@router.post("/signup", response_model=UserOut)
def signup(user_in: SignupRequest, db: Session = Depends(get_db)):
    existing = crud.user.get_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # ONLY allow HR + ADMIN signup
    if user_in.role not in ["HR", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR and ADMIN are allowed to signup"
        )

    user = crud.user.create(db, user_in)
    return user

# ----------------------------
# LOGIN (SIMPLE JSON)
# ----------------------------
@router.post("/login", response_model=Token)
def login(user_in: LoginRequest,response: Response, db: Session = Depends(get_db)):
    print("\n=== LOGIN ATTEMPT ===")
    print(f"Email: {user_in.email}")

    user = crud.user.get_by_email(db, email=user_in.email)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")

    access_token = create_access_token({"sub": str(user.id)})
    print(f"Token created: {access_token[:20]}...")

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # Can't be accessed by JavaScript
        max_age=3600,   # 1 hour
        expires=3600,
        path="/",
        samesite="lax",
        secure=False,
    )
    print("Cookie set in response")
    print(f"Response headers will include: set-cookie")

    return {"access_token": access_token, "token_type": "bearer"}


# ----------------------------
# GET CURRENT USER (Bearer Token)
# ----------------------------
def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> User:
    token = None
    
    # 1. Try to get token from Authorization header (Bearer token)
    if credentials:
        token = credentials.credentials
        print(f"Token from header: {token[:20]}...")  # Debug
    
    # 2. If no header token, try cookie
    if not token:
        token = request.cookies.get("access_token")
        print(f"Token from cookie: {token[:20] if token else 'None'}")  # Debug
    
    # 3. If still no token, raise error
    if not token:
        print("No token found in header or cookie")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 4. Validate the token
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
            
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    # 5. Get user from database
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user
# ----------------------------
# ME
# ----------------------------
@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
