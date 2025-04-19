"""
Defines authentication-related API routes such as user signup and login.
"""

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import SignupDto, LoginDto
from .services.auth import AuthService
from ...utils.dependencies import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup")
async def signup(signup_dto: SignupDto, session: AsyncSession = Depends(get_db)):
    """
    Handles user signup.

    Accepts user data, validates input, creates a new user, and returns a success message
    along with user details.
    """
    auth_service = AuthService(session)
    signup_response = await auth_service.signup(signup_dto)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Signup successful", "data": signup_response},
    )
