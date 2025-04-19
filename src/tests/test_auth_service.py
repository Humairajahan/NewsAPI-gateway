import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.auth.services.auth import AuthService
from src.modules.auth.schema import SignupDto
from src.modules.user.entity import User


class TestAuthService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.db = AsyncMock(spec=AsyncSession)
        self.auth_service = AuthService(self.db)

    @patch(
        "src.modules.auth.services.auth.jwt_service.encode_password",
        return_value="hashedpass",
    )
    async def test_signup_success(self, mock_encode):
        signup_data = SignupDto(
            username="testuser",
            email="test@example.com",
            password="password123",
            confirm_password="password123",
        )

        # Create mock result for db.execute
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        self.db.execute.return_value = mock_result

        self.db.add = MagicMock()
        self.db.commit = AsyncMock()
        self.db.refresh = AsyncMock()

        result = await self.auth_service.signup(signup_data)
        self.assertIn("user", result)
        self.assertEqual(result["user"]["email"], "test@example.com")

    async def test_signup_passwords_do_not_match(self):
        signup_data = SignupDto(
            username="testuser",
            email="test@example.com",
            password="pass1",
            confirm_password="pass2",
        )
        with self.assertRaises(HTTPException) as context:
            await self.auth_service.signup(signup_data)
        self.assertEqual(context.exception.detail, "Passwords do not match")

    async def test_signup_user_already_exists(self):
        signup_data = SignupDto(
            username="testuser",
            email="test@example.com",
            password="password123",
            confirm_password="password123",
        )

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = (
            MagicMock()
        )  # Simulate existing user
        self.db.execute.return_value = mock_result

        with self.assertRaises(HTTPException) as context:
            await self.auth_service.signup(signup_data)
        self.assertEqual(
            context.exception.detail, "User with this email already exists"
        )

    @patch(
        "src.modules.auth.services.auth.jwt_service.validate_password",
        return_value=True,
    )
    @patch(
        "src.modules.auth.services.auth.jwt_service.generate_jwt_token",
        return_value="token",
    )
    @patch(
        "src.modules.auth.services.auth.jwt_service.generate_refresh_token",
        return_value="refresh",
    )
    async def test_login_success(self, mock_refresh, mock_token, mock_validate):
        form_data = OAuth2PasswordRequestForm(
            username="test@example.com", password="password", scope=""
        )
        user_mock = MagicMock()
        user_mock.id = 1
        user_mock.email = "test@example.com"
        user_mock.username = "testuser"
        user_mock.password = "hashedpass"

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = user_mock
        self.db.execute.return_value = mock_result

        result = await self.auth_service.login(form_data)
        self.assertIn("access_token", result)
        self.assertEqual(result["token_type"], "bearer")

    async def test_login_user_not_found(self):
        form_data = OAuth2PasswordRequestForm(
            username="notfound@example.com", password="password", scope=""
        )

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        self.db.execute.return_value = mock_result

        with self.assertRaises(HTTPException) as context:
            await self.auth_service.login(form_data)
        self.assertEqual(
            context.exception.detail, "User with this email does not exist"
        )

    @patch(
        "src.modules.auth.services.auth.jwt_service.validate_password",
        return_value=False,
    )
    async def test_login_invalid_password(self, mock_validate):
        form_data = OAuth2PasswordRequestForm(
            username="test@example.com", password="wrongpass", scope=""
        )
        user_mock = MagicMock()
        user_mock.id = 1
        user_mock.email = "test@example.com"
        user_mock.username = "testuser"
        user_mock.password = "hashedpass"

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = user_mock
        self.db.execute.return_value = mock_result

        with self.assertRaises(HTTPException) as context:
            await self.auth_service.login(form_data)
        self.assertEqual(context.exception.detail, "Invalid user credentials")
