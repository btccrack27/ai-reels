from typing import Optional
from datetime import datetime, timedelta
import uuid
from ...domain.interfaces.content_repository import IContentRepository
from ...domain.interfaces.user_repository import IUserRepository
from ...domain.interfaces.subscription_repository import ISubscriptionRepository
from ...domain.interfaces.usage_repository import IUsageRepository
from ...domain.entities.content import Content, ContentType, ContentStatus
from ...domain.entities.broll import BRollContent
from ...domain.services.rate_limiter import RateLimiter
from ...domain.services.content_validator import ContentValidator
from ...infrastructure.ai_services.claude_service import ClaudeService
from ..dto.content_dto import GenerateBRollRequestDTO, BRollResponseDTO


class GenerateBRollUseCase:
    """Use Case für B-Roll Ideas-Generierung (10 Ideen)"""

    def __init__(
        self,
        content_repository: IContentRepository,
        user_repository: IUserRepository,
        subscription_repository: ISubscriptionRepository,
        usage_repository: IUsageRepository,
        claude_service: ClaudeService,
        rate_limiter: RateLimiter,
        content_validator: ContentValidator
    ):
        self.content_repo = content_repository
        self.user_repo = user_repository
        self.subscription_repo = subscription_repository
        self.usage_repo = usage_repository
        self.claude_service = claude_service
        self.rate_limiter = rate_limiter
        self.content_validator = content_validator

    async def execute(self, request: GenerateBRollRequestDTO) -> BRollResponseDTO:
        """Generiert 10 B-Roll Ideas (3-5 Wörter)"""

        # 1. User & Subscription laden
        user = await self.user_repo.get_by_id(request.user_id)
        if not user:
            raise ValueError(f"User {request.user_id} nicht gefunden")

        subscription = await self.subscription_repo.get_by_user_id(request.user_id)
        if not subscription:
            raise ValueError(f"Keine Subscription für User {request.user_id}")

        # 2. Rate-Limits prüfen
        period_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        period_end = (period_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

        current_usage = await self.usage_repo.get_current_usage(
            user_id=request.user_id,
            content_type=ContentType.BROLL,
            period_start=period_start,
            period_end=period_end
        )

        can_generate, error_message = self.rate_limiter.can_generate(
            subscription=subscription,
            content_type=ContentType.BROLL,
            current_usage=current_usage
        )

        if not can_generate:
            raise PermissionError(error_message)

        # 3. Claude API aufrufen
        try:
            broll_content = await self.claude_service.generate_broll_ideas(
                prompt=request.prompt,
                context=request.context
            )
        except Exception as e:
            raise Exception(f"Fehler bei B-Roll-Generierung: {str(e)}")

        # 4. Content validieren
        try:
            broll_content.validate()
        except Exception as e:
            raise Exception(f"Validierung fehlgeschlagen: {str(e)}")

        # 5. In Datenbank speichern
        content = Content(
            id=str(uuid.uuid4()),
            user_id=request.user_id,
            type=ContentType.BROLL,
            status=ContentStatus.COMPLETED,
            data={
                "ideas": broll_content.ideas
            },
            prompt=request.prompt,
            version=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={
                "context": request.context
            }
        )

        saved_content = await self.content_repo.create(content)

        # 6. Usage-Counter erhöhen
        await self.usage_repo.increment_usage(
            user_id=request.user_id,
            content_type=ContentType.BROLL,
            period_start=period_start,
            period_end=period_end
        )

        # 7. Response zurückgeben
        return BRollResponseDTO(
            id=saved_content.id,
            ideas=broll_content.ideas,
            prompt=request.prompt,
            created_at=saved_content.created_at
        )
