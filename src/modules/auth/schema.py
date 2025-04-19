"""
Defines Pydantic data transfer objects (DTOs)
for authentication-related requests.
"""

from pydantic import BaseModel, EmailStr


class SignupDto(BaseModel):
    """
    Data transfer object for user signup requests.
    """

    username: str
    email: EmailStr
    password: str
    confirm_password: str
