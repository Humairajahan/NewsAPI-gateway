"""
Authentication middleware utility.

Provides a FastAPI dependency that validates JWT tokens from the `Authorization` header,
retrieves the associated user from the database, and injects the user into route handlers.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..modules.auth.services.jwt import JwtService
from ..modules.user.entity import User
from ..utils.dependencies import get_db


jwt_service = JwtService()
security = HTTPBearer()


async def get_user(
    authorization: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependency. Extracts and verifies a JWT from the Authorization header.

    Verifies the token's validity and fetches the corresponding user from the database.
    Raises appropriate HTTP exceptions if the token is invalid, expired, or the user is not found.
    """
    if authorization.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")

    token = authorization.credentials

    try:
        payload = jwt_service.verify_jwt_token(token)
        user_id = int(payload.get("sub"))

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: no user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_exists = await session.execute(select(User).where(User.id == user_id))
        user = user_exists.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    except ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: expired: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
