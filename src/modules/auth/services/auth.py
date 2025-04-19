"""
Handles user authentication services including signup and login.
"""

from fastapi import Response, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from .jwt import JwtService
from ..schema import SignupDto, LoginDto
from ...user.entity import User

jwt_service = JwtService()


class AuthService:
    """
    Service layer for handling user authentication logic such as
    registration, login, and token issuance.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def unified_auth_response(user: User) -> dict:
        """
        Formats the user object into a unified
        response dictionary excluding sensitive fields.
        """
        return {
            "id": user.id,
            "uuid": jsonable_encoder(user.uuid),
            "username": user.username,
            "email": user.email,
        }

    async def signup(self, signup_dto: SignupDto):
        """
        Registers a new user.
        """
        # EDGE CASE: PASSWORDS DO NOT MATCH
        if signup_dto.password != signup_dto.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        # EDGE CASE: USER WITH THIS EMAIL ALREADY EXISTS
        user_exists = await self.db.execute(
            select(User).where(User.email == signup_dto.email)
        )
        user = user_exists.scalar_one_or_none()
        if user:
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )

        # ENCODE PASSWORD
        hashed_password = jwt_service.encode_password(signup_dto.password)

        # CREATE USER OBJECT
        user = User(
            username=signup_dto.username,
            email=signup_dto.email,
            password=hashed_password,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return {
            "user": AuthService.unified_auth_response(user),
        }
