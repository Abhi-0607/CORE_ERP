#hey

from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config import settings

def create_access_token(data: dict, expires_minutes: int | None = None):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
