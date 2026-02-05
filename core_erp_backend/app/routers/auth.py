from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database import get_db
from app.config import settings
from app.schemas.users import UserOut, Token, SignupRequest, LoginRequest
from app.crud.users import get_user_by_email, create_user
from app.utils.security import verify_password
from app.utils.token import create_access_token
from app.models.users import User

router = APIRouter(prefix="/auth", tags=["Auth"])

bearer_scheme = HTTPBearer()


# ----------------------------
# SIGNUP
# ----------------------------
@router.post("/signup", response_model=UserOut)
def signup(user_in: SignupRequest, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
        # ONLY allow HR signup for now
    if user_in.role not in ["HR", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR and ADMIN are allowed to signup"
        )

    user = create_user(db, user_in)
    return user

    user = create_user(db, user_in)
    return user


# ----------------------------
# LOGIN (SIMPLE JSON)
# ----------------------------
@router.post("/login", response_model=Token)
def login(user_in: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_in.email)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")

    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# ----------------------------
# GET CURRENT USER (Bearer Token)
# ----------------------------
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials

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


# ----------------------------
# ME
# ----------------------------
@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
