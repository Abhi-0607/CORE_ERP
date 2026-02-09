from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.users import SignupRequest
from app.utils.security import hash_password


class CRUDUser:
    def get(self, db: Session, id: int):
        return db.query(User).filter(User.id == id).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, user_in: SignupRequest):
        user = User(
            email=user_in.email,
            role=user_in.role.value if hasattr(user_in.role, "value") else user_in.role,
            full_name=user_in.full_name,
            hashed_password=hash_password(user_in.password),
            is_active=True,
            must_change_password=False,
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user


user = CRUDUser()