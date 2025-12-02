from datetime import datetime, timedelta
import uuid
from passlib.context import CryptContext
import jwt
import os
from ...domain.interfaces.user_repository import IUserRepository
from ...domain.interfaces.subscription_repository import ISubscriptionRepository
from ...domain.entities.user import User, UserRole
from ...domain.entities.subscription import Subscription, SubscriptionPlan, SubscriptionStatus
from ..dto.auth_dto import RegisterRequestDTO, RegisterResponseDTO, UserResponseDTO, AuthTokensDTO


class RegisterUserUseCase:
    """
    Use Case für User-Registrierung.

    Flow:
    1. Email-Validierung (unique check)
    2. Password hashen
    3. User erstellen
    4. FREE Subscription erstellen
    5. JWT Tokens generieren
    6. Response zurückgeben
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        subscription_repository: ISubscriptionRepository
    ):
        self.user_repo = user_repository
        self.subscription_repo = subscription_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.jwt_secret = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    async def execute(self, request: RegisterRequestDTO) -> RegisterResponseDTO:
        """
        Registriert neuen User mit FREE Subscription.

        Args:
            request: RegisterRequestDTO mit email, name, password

        Returns:
            RegisterResponseDTO mit User und Tokens

        Raises:
            ValueError: Wenn Email bereits existiert oder Validierung fehlschlägt
        """
        # 1. Email-Validierung
        existing_user = await self.user_repo.get_by_email(request.email)
        if existing_user:
            raise ValueError(f"Email {request.email} bereits registriert")

        if not self._validate_email(request.email):
            raise ValueError("Ungültige Email-Adresse")

        if not self._validate_password(request.password):
            raise ValueError("Password muss mindestens 8 Zeichen haben")

        # 2. Password hashen
        password_hash = self.pwd_context.hash(request.password)

        # 3. User erstellen
        user_id = str(uuid.uuid4())
        user = User(
            id=user_id,
            email=request.email,
            name=request.name,
            role=UserRole.FREE,
            subscription_id=None,  # Wird nach Subscription-Erstellung gesetzt
            stripe_customer_id=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True
        )

        # Password hash hinzufügen (nicht Teil der Domain Entity)
        # In production würde man password_hash in UserModel speichern
        created_user = await self.user_repo.create(user)

        # 4. FREE Subscription erstellen
        subscription_id = str(uuid.uuid4())
        now = datetime.now()
        period_end = (now + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

        subscription = Subscription(
            id=subscription_id,
            user_id=created_user.id,
            plan=SubscriptionPlan.FREE,
            status=SubscriptionStatus.ACTIVE,
            stripe_subscription_id=None,  # FREE hat keine Stripe Subscription
            current_period_start=now,
            current_period_end=period_end,
            cancel_at_period_end=False
        )

        created_subscription = await self.subscription_repo.create(subscription)

        # User mit subscription_id updaten
        updated_user = await self.user_repo.update(
            user_id=created_user.id,
            subscription_id=created_subscription.id
        )

        # 5. JWT Tokens generieren
        tokens = self._generate_tokens(updated_user)

        # 6. Response zurückgeben
        return RegisterResponseDTO(
            user=UserResponseDTO(
                id=updated_user.id,
                email=updated_user.email,
                name=updated_user.name,
                role=updated_user.role,
                subscription_id=updated_user.subscription_id,
                stripe_customer_id=updated_user.stripe_customer_id,
                is_active=updated_user.is_active,
                created_at=updated_user.created_at
            ),
            tokens=tokens
        )

    def _validate_email(self, email: str) -> bool:
        """Einfache Email-Validierung"""
        return "@" in email and "." in email

    def _validate_password(self, password: str) -> bool:
        """Password muss mindestens 8 Zeichen haben"""
        return len(password) >= 8

    def _generate_tokens(self, user: User) -> AuthTokensDTO:
        """Generiert Access & Refresh Tokens"""
        now = datetime.now()

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
