from typing import Optional
from datetime import datetime, timedelta
import uuid
from ...domain.interfaces.content_repository import IContentRepository
from ...domain.interfaces.user_repository import IUserRepository
from ...domain.interfaces.subscription_repository import ISubscriptionRepository
from ...domain.interfaces.usage_repository import IUsageRepository
from ...domain.entities.content import Content, ContentType, ContentStatus
from ...domain.entities.script import ScriptContent
from ...domain.services.rate_limiter import RateLimiter
from ...domain.services.content_validator import ContentValidator
from ...infrastructure.ai_services.claude_service import ClaudeService
from ..dto.content_dto import GenerateScriptRequestDTO, ScriptResponseDTO, SceneDTO


class GenerateScriptUseCase:
    """Use Case für Script-Generierung (2-4 Szenen)"""

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

    async def execute(self, request: GenerateScriptRequestDTO) -> ScriptResponseDTO:
        """Generiert Reel-Script mit 2-4 Szenen"""

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
            content_type=ContentType.SCRIPT,
            period_start=period_start,
            period_end=period_end
        )

        can_generate, error_message = self.rate_limiter.can_generate(
            subscription=subscription,
            content_type=ContentType.SCRIPT,
            current_usage=current_usage
        )

        if not can_generate:
            raise PermissionError(error_message)

        # 3. Claude API aufrufen
        try:
            script_content = await self.claude_service.generate_script(
                prompt=request.prompt,
                context=request.context,
                duration_seconds=request.duration_seconds
            )
        except Exception as e:
            raise Exception(f"Fehler bei Script-Generierung: {str(e)}")

        # 4. Content validieren
        try:
            script_content.validate()
        except Exception as e:
            raise Exception(f"Validierung fehlgeschlagen: {str(e)}")

        # 5. In Datenbank speichern
        content = Content(
            id=str(uuid.uuid4()),
            user_id=request.user_id,
            type=ContentType.SCRIPT,
            status=ContentStatus.COMPLETED,
            data={
                "scenes": [
                    {
                        "scene_number": scene.scene_number,
                        "type": scene.type,
                        "text": scene.text,
                        "visual_description": scene.visual_description,
                        "duration_seconds": scene.duration_seconds
                    }
                    for scene in script_content.scenes
                ],
                "cta": script_content.cta,
                "total_duration": script_content.total_duration
            },
            prompt=request.prompt,
            version=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={
                "context": request.context,
                "duration_seconds": request.duration_seconds
            }
        )

        saved_content = await self.content_repo.create(content)

        # 6. Usage-Counter erhöhen
        await self.usage_repo.increment_usage(
            user_id=request.user_id,
            content_type=ContentType.SCRIPT,
            period_start=period_start,
            period_end=period_end
        )

        # 7. Response zurückgeben
        return ScriptResponseDTO(
            id=saved_content.id,
            scenes=[
                SceneDTO(
                    scene_number=scene.scene_number,
                    type=scene.type,
                    text=scene.text,
                    visual_description=scene.visual_description,
                    duration_seconds=scene.duration_seconds
                )
                for scene in script_content.scenes
            ],
            cta=script_content.cta,
            total_duration=script_content.total_duration,
            prompt=request.prompt,
            created_at=saved_content.created_at
        )
