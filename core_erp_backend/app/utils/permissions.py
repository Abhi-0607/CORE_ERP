from fastapi import HTTPException, status
from app.constants.roles import UserRole


class Permission:
    @staticmethod
    def _normalize_role(role) -> str:
        """
        Supports both:
        - Enum role (UserRole.ADMIN)
        - String role ("ADMIN")
        """
        if role is None:
            return ""

        if hasattr(role, "value"):  # Enum
            return str(role.value).strip().upper()

        return str(role).strip().upper()

    @classmethod
    def require_roles(cls, user, allowed_roles: list[UserRole]):
        user_role = cls._normalize_role(user.role)
        allowed = {cls._normalize_role(r) for r in allowed_roles}

        if user_role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform this action"
            )
