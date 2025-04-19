import unittest
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from src.config import APP_SECRET, ALGORITHM, APP_EXPIRES_IN
from src.modules.auth.services.jwt import JwtService
from src.modules.user.entity import User


class JwtServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.jwt_service = JwtService()
        self.user = User(id=1, email="test@example.com")

    def test_encode_password_and_validate_successfully(self):
        password = "my_secure_password"
        hashed = self.jwt_service.encode_password(password)
        self.assertNotEqual(password, hashed)
        self.assertTrue(self.jwt_service.validate_password(password, hashed))

    def test_validate_password_fails_with_wrong_password(self):
        password = "correct_password"
        hashed = self.jwt_service.encode_password(password)
        self.assertFalse(self.jwt_service.validate_password("wrong_password", hashed))

    def test_generate_jwt_token_contains_expected_payload(self):
        token = self.jwt_service.generate_jwt_token(self.user)
        decoded = jwt.decode(token, APP_SECRET, algorithms=[ALGORITHM])
        self.assertEqual(decoded["sub"], str(self.user.id))
        self.assertEqual(decoded["email"], self.user.email)
        self.assertIn("exp", decoded)

    def test_generate_refresh_token_contains_expected_payload(self):
        token = self.jwt_service.generate_refresh_token(self.user)
        decoded = jwt.decode(token, APP_SECRET, algorithms=[ALGORITHM])
        self.assertEqual(decoded["sub"], str(self.user.id))
        self.assertEqual(decoded["email"], self.user.email)
        self.assertIn("exp", decoded)

    def test_verify_jwt_token_returns_payload(self):
        token = self.jwt_service.generate_jwt_token(self.user)
        payload = self.jwt_service.verify_jwt_token(token)
        self.assertEqual(payload["email"], self.user.email)

    def test_verify_jwt_token_raises_JWTError_for_invalid_token(self):
        with self.assertRaises(JWTError):
            self.jwt_service.verify_jwt_token("invalid.token.payload")

    def test_verify_jwt_token_raises_ExpiredSignatureError(self):
        expired_token = jwt.encode(
            {
                "sub": str(self.user.id),
                "email": self.user.email,
                "exp": datetime.utcnow() - timedelta(seconds=1),
            },
            APP_SECRET,
            algorithm=ALGORITHM,
        )

        with self.assertRaises(ExpiredSignatureError):
            self.jwt_service.verify_jwt_token(expired_token)
