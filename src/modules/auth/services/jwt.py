"""
Provides JWT-based authentication services including
token generation, verification, and password hashing utilities.
"""

from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from ...user.entity import User
from ....config import ALGORITHM, APP_SECRET, APP_EXPIRES_IN, REFRESH_TOKEN_EXPIRES_IN

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JwtService:
    """
    Service layer for handling password encryption and JWT token operations.
    """

    def __init__(self):
        pass

    def encode_password(self, password: str) -> str:
        """
        Hashes a plaintext password using bcrypt.
        """
        return pwd_context.hash(password)

    def validate_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Validates the stored hashed password with the plain password.
        """
        return pwd_context.verify(plain_password, hashed_password)

    def generate_jwt_token(self, user: User) -> str:
        """
        Generates JWT access token expiring in 1 hour (3600 sec)
        """
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(seconds=APP_EXPIRES_IN),
        }
        token = jwt.encode(payload, APP_SECRET, algorithm=ALGORITHM)
        return token

    def generate_refresh_token(self, user: User) -> str:
        """
        Generates refresh token expiring in 7 days (604800 sec)
        """
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(seconds=REFRESH_TOKEN_EXPIRES_IN),
        }
        token = jwt.encode(payload, APP_SECRET, algorithm=ALGORITHM)
        return token

    def verify_jwt_token(self, token: str) -> dict:
        """
        Decodes and verifies a JWT access token.
        """
        try:
            payload = jwt.decode(token, APP_SECRET, algorithms=[ALGORITHM])
            return payload
        except JWTError as exc:
            raise exc
        except ExpiredSignatureError as exc:
            raise exc
