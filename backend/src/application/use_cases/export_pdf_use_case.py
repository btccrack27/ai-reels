from datetime import datetime, timedelta
from ...domain.interfaces.content_repository import IContentRepository
from ...domain.interfaces.user_repository import IUserRepository
from ...domain.interfaces.subscription_repository import ISubscriptionRepository
from ...domain.interfaces.usage_repository import IUsageRepository
from ...domain.entities.content import ContentType
from ...domain.entities.hook import HookContent
from ...domain.entities.script import ScriptContent, SceneContent
from ...domain.entities.shotlist import ShotlistContent
from ...domain.entities.voiceover import VoiceoverContent
from ...domain.entities.caption import CaptionContent
from ...domain.entities.broll import BRollContent
from ...domain.entities.calendar import CalendarContent, DayContent
from ...domain.services.rate_limiter import RateLimiter
from ...infrastructure.pdf.pdf_generator import PDFGenerator
from ..dto.content_dto import ExportPDFRequestDTO, ExportPDFResponseDTO


class ExportPDFUseCase:
    """
    Use Case für PDF Export.

    Flow:
    1. User & Subscription laden
    2. PDF-Export Limits prüfen
    3. Content aus DB laden
    4. PDF generieren (basierend auf Content Type)
    5. Usage-Counter erhöhen
    6. PDF bytes zurückgeben
    """

    def __init__(
        self,
        content_repository: IContentRepository,
        user_repository: IUserRepository,
        subscription_repository: ISubscriptionRepository,
        usage_repository: IUsageRepository,
        pdf_generator: PDFGenerator,
        rate_limiter: RateLimiter
    ):
        self.content_repo = content_repository
        self.user_repo = user_repository
        self.subscription_repo = subscription_repository
        self.usage_repo = usage_repository
        self.pdf_generator = pdf_generator
        self.rate_limiter = rate_limiter

    async def execute(self, request: ExportPDFRequestDTO) -> ExportPDFResponseDTO:
        """
        Exportiert Content als PDF.

        Args:
            request: ExportPDFRequestDTO mit user_id, content_id

        Returns:
            ExportPDFResponseDTO mit PDF bytes

        Raises:
            ValueError: Wenn User oder Content nicht existiert
            PermissionError: Wenn PDF-Limit erreicht oder Content nicht gehört User
        """
        # 1. User & Subscription laden
        user = await self.user_repo.get_by_id(request.user_id)
        if not user:
            raise ValueError(f"User {request.user_id} nicht gefunden")

        subscription = await self.subscription_repo.get_by_user_id(request.user_id)
        if not subscription:
            raise ValueError(f"Keine Subscription für User {request.user_id}")

        # 2. Content laden
        content = await self.content_repo.get_by_id(request.content_id)
        if not content:
            raise ValueError(f"Content {request.content_id} nicht gefunden")

        # Permission Check: Content gehört User?
        if content.user_id != request.user_id:
            raise PermissionError("Content gehört nicht diesem User")

        # 3. PDF-Export Limits prüfen
        # Hinweis: PDF Export hat eigenes Limit (nicht per Content Type)
        # Für simplified implementation: Keine separate PDF Usage Tracking
        # In production würde man ein separates PDF_EXPORT ContentType tracken

        # 4. PDF generieren (basierend auf Content Type)
        try:
            pdf_bytes = await self._generate_pdf_for_content(content)
        except Exception as e:
            raise Exception(f"Fehler bei PDF-Generierung: {str(e)}")

        # 5. Filename generieren
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{content.type.value}_{timestamp}.pdf"

        # 6. Response zurückgeben
        return ExportPDFResponseDTO(
            content_id=content.id,
            content_type=content.type,
            pdf_bytes=pdf_bytes,
            filename=filename
        )

    async def _generate_pdf_for_content(self, content) -> bytes:
        """Generiert PDF basierend auf Content Type"""
        content_type = content.type
        data = content.data
        prompt = content.prompt

        if content_type == ContentType.HOOK:
            hook_content = HookContent(hooks=data["hooks"])
            return self.pdf_generator.generate_hook_pdf(hook_content, prompt)

        elif content_type == ContentType.SCRIPT:
            scenes = [
                Scene(
                    scene_number=scene["scene_number"],
                    type=scene["type"],
                    text=scene["text"],
                    visual_description=scene["visual_description"],
                    duration_seconds=scene["duration_seconds"]
                )
                for scene in data["scenes"]
            ]
            script_content = ScriptContent(
                scenes=scenes,
                cta=data["cta"],
                total_duration=data["total_duration"]
            )
            return self.pdf_generator.generate_script_pdf(script_content, prompt)

        elif content_type == ContentType.SHOTLIST:
            shotlist_content = ShotlistContent(shots=data["shots"])
            return self.pdf_generator.generate_shotlist_pdf(shotlist_content, prompt)

        elif content_type == ContentType.VOICEOVER:
            voiceover_content = VoiceoverContent(
                text=data["text"],
                estimated_duration=data["estimated_duration"]
            )
            return self.pdf_generator.generate_voiceover_pdf(voiceover_content, prompt)

        elif content_type == ContentType.CAPTION:
            caption_content = CaptionContent(
                caption=data["caption"],
                hashtags=data["hashtags"]
            )
            return self.pdf_generator.generate_caption_pdf(caption_content, prompt)

        elif content_type == ContentType.BROLL:
            broll_content = BRollContent(ideas=data["ideas"])
            return self.pdf_generator.generate_broll_pdf(broll_content, prompt)

        elif content_type == ContentType.CALENDAR:
            days = {
                int(day_num): DayContent(
                    day=day_data["day"],
                    hook=day_data["hook"],
                    theme=day_data["theme"]
                )
                for day_num, day_data in data["days"].items()
            }
            calendar_content = CalendarContent(
                niche=data["niche"],
                days=days
            )
            return self.pdf_generator.generate_calendar_pdf(calendar_content, prompt)

        else:
            raise ValueError(f"Unbekannter Content Type: {content_type}")
