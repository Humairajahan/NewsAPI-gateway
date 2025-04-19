"""
Defines authentication-related API routes such as user signup and login.
"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import SignupDto
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


@router.post("/login")
async def login(
    req: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
):
    """
    Handles user login.

    Authenticates a user based on email/username and password.
    On success, returns user details along with access and refresh tokens.
    """
    auth_service = AuthService(session)
    login_response = await auth_service.login(req)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Login successful", "data": login_response},
    )
