#hey

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # ERP Fields
    employee_id = Column(String(50), unique=True, index=True, nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)

    # Roles: ADMIN, HR, MANAGER, EMPLOYEE
    role = Column(String(30), nullable=False)

    # Optional but useful in ERP
    full_name = Column(String(255), nullable=True)

    # Auth
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # If HR creates account, employee must change password on first login
    must_change_password = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    last_login = Column(DateTime(timezone=True), nullable=True)