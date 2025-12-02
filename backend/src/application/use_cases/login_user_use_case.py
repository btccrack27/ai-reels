from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
import os
from ...domain.interfaces.user_repository import IUserRepository
from ...domain.entities.user import User
from ..dto.auth_dto import LoginRequestDTO, LoginResponseDTO, UserResponseDTO, AuthTokensDTO


class LoginUserUseCase:
    """
    Use Case für User-Login.

    Flow:
    1. User per Email laden
    2. Password verifizieren
    3. JWT Tokens generieren
    4. Response zurückgeben
    """

    def __init__(self, user_repository: IUserRepository):
        self.user_repo = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.jwt_secret = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    async def execute(self, request: LoginRequestDTO) -> LoginResponseDTO:
        """
        Loggt User ein und gibt Tokens zurück.

        Args:
            request: LoginRequestDTO mit email, password

        Returns:
            LoginResponseDTO mit User und Tokens

        Raises:
            ValueError: Wenn Email oder Password falsch
            PermissionError: Wenn User nicht aktiv
        """
        # 1. User per Email laden
        user = await self.user_repo.get_by_email(request.email)
        if not user:
            raise ValueError("Email oder Password falsch")

        # 2. Password verifizieren
        if not self.pwd_context.verify(request.password, user.password_hash):
            raise ValueError("Email oder Password falsch")

        # User aktiv?
        if not user.is_active:
            raise PermissionError("User-Account ist deaktiviert")

        # 3. JWT Tokens generieren
        tokens = self._generate_tokens(user)

        # 4. Response zurückgeben
        return LoginResponseDTO(
            user=UserResponseDTO(
                id=user.id,
                email=user.email,
                name=user.name,
                role=user.role,
                subscription_id=user.subscription_id,
                stripe_customer_id=user.stripe_customer_id,
                is_active=user.is_active,
                created_at=user.created_at
            ),
            tokens=tokens
        )

    def _generate_tokens(self, user: User) -> AuthTokensDTO:
        """Generiert Access & Refresh Tokens"""
        now = datetime.now(timezone.utc)

        # Access Token (1 Stunde)
        access_token_payload = {
            "sub": user.id,
            "email": user.email,
            "role": user.role.value,
            "type": "access",
            "iat": now,
            "exp": now + timedelta(hours=1)
        }
        access_token = jwt.encode(access_token_payload, self.jwt_secret, algorithm=self.jwt_algorithm)

        # Refresh Token (7 Tage)
        refresh_token_payload = {
            "sub": user.id,
            "type": "refresh",
            "iat": now,
            "exp": now + timedelta(days=7)
        }
        refresh_token = jwt.encode(refresh_token_payload, self.jwt_secret, algorithm=self.jwt_algorithm)

        return AuthTokensDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=3600  # 1 Stunde in Sekunden
        )
