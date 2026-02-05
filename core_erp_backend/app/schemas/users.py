#hey

from typing import Optional
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from app.constants.roles import UserRole

# bcrypt max = 72 bytes
def _validate_bcrypt_password(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password too long (bcrypt max is 72 bytes).")
    if len(password) < 6:
        raise ValueError("Password too short (minimum 6 characters).")
    return password


# -------------------------
# SIGNUP (ONLY HR/ADMIN/MANAGER)
# -------------------------
class SignupRequest(BaseModel):
    email: EmailStr
    role: UserRole
    full_name: Optional[str] = None
    password: str
    confirm_password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        return _validate_bcrypt_password(v)

    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, v: str):
        return _validate_bcrypt_password(v)


# -------------------------
# LOGIN (for all users)
# -------------------------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        return _validate_bcrypt_password(v)

# -------------------------
# RESPONSE USER (safe output)
# -------------------------
class UserOut(BaseModel):
    id: int
    employee_id: Optional[str] = None
    email: EmailStr
    role: str
    full_name: Optional[str] = None
    is_active: bool
    must_change_password: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
