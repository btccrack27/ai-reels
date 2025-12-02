from datetime import datetime, timedelta
from ...domain.interfaces.user_repository import IUserRepository
from ...domain.interfaces.subscription_repository import ISubscriptionRepository
from ...domain.interfaces.usage_repository import IUsageRepository
from ...domain.entities.content import ContentType
from ...domain.entities.subscription import PLAN_LIMITS
from ..dto.subscription_dto import SubscriptionStatusResponseDTO, SubscriptionResponseDTO, UsageLimitDTO, CurrentUsageDTO


class GetSubscriptionStatusUseCase:
    """
    Use Case für Subscription Status Abfrage.

    Returns:
    - Subscription Details
    - Plan Limits
    - Current Usage
    - Remaining Quota
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        subscription_repository: ISubscriptionRepository,
        usage_repository: IUsageRepository
    ):
        self.user_repo = user_repository
        self.subscription_repo = subscription_repository
        self.usage_repo = usage_repository

    async def execute(self, user_id: str) -> SubscriptionStatusResponseDTO:
        """
        Gibt vollständigen Subscription Status zurück.

        Args:
            user_id: User ID

        Returns:
            SubscriptionStatusResponseDTO mit allen Infos

        Raises:
            ValueError: Wenn User oder Subscription nicht existiert
        """
        # 1. User laden
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} nicht gefunden")

        # 2. Subscription laden
        subscription = await self.subscription_repo.get_by_user_id(user_id)
        if not subscription:
            raise ValueError(f"Keine Subscription für User {user_id}")

        # 3. Plan Limits holen
        plan_limits = PLAN_LIMITS[subscription.plan]

        # 4. Current Usage laden
        period_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        period_end = (period_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

        # Usage für jeden Content Type laden
        hook_usage = await self.usage_repo.get_current_usage(
            user_id=user_id,
            content_type=ContentType.HOOK,
            period_start=period_start,
            period_end=period_end
        )

        script_usage = await self.usage_repo.get_current_usage(
            user_id=user_id,
            content_type=ContentType.SCRIPT,
            period_start=period_start,
            period_end=period_end
        )

        shotlist_usage = await self.usage_repo.get_current_usage(
            user_id=user_id,
            content_type=ContentType.SHOTLIST,
            period_start=period_start,
            period_end=period_end
        )

        voiceover_usage = await self.usage_repo.get_current_usage(
            user_id=user_id,
            content_type=ContentType.VOICEOVER,
            period_start=period_start,
            period_end=period_end
        )

        caption_usage = await self.usage_repo.get_current_usage(
            user_id=user_id,
            content_type=ContentType.CAPTION,
            period_start=period_start,
            period_end=period_end
        )

        broll_usage = await self.usage_repo.get_current_usage(
            user_id=user_id,
            content_type=ContentType.BROLL,
            period_start=period_start,
            period_end=period_end
        )

        calendar_usage = await self.usage_repo.get_current_usage(
            user_id=user_id,
            content_type=ContentType.CALENDAR,
            period_start=period_start,
            period_end=period_end
        )

        # 5. Current Usage DTO erstellen
        current_usage = CurrentUsageDTO(
            hook=hook_usage.count if hook_usage else 0,
            script=script_usage.count if script_usage else 0,
            shotlist=shotlist_usage.count if shotlist_usage else 0,
            voiceover=voiceover_usage.count if voiceover_usage else 0,
            caption=caption_usage.count if caption_usage else 0,
            broll=broll_usage.count if broll_usage else 0,
            calendar=calendar_usage.count if calendar_usage else 0,
            pdf=0  # PDF Usage wird separat getrackt
        )

        # 6. Remaining berechnen
        remaining = {
            "hook": max(0, plan_limits.hook_per_month - current_usage.hook) if plan_limits.hook_per_month != -1 else -1,
            "script": max(0, plan_limits.script_per_month - current_usage.script) if plan_limits.script_per_month != -1 else -1,
            "shotlist": max(0, plan_limits.shotlist_per_month - current_usage.shotlist) if plan_limits.shotlist_per_month != -1 else -1,
            "voiceover": max(0, plan_limits.voiceover_per_month - current_usage.voiceover) if plan_limits.voiceover_per_month != -1 else -1,
            "caption": max(0, plan_limits.caption_per_month - current_usage.caption) if plan_limits.caption_per_month != -1 else -1,
            "broll": max(0, plan_limits.broll_per_month - current_usage.broll) if plan_limits.broll_per_month != -1 else -1,
            "calendar": max(0, plan_limits.calendar_per_month - current_usage.calendar) if plan_limits.calendar_per_month != -1 else -1,
            "pdf": max(0, plan_limits.pdf_per_month - current_usage.pdf) if plan_limits.pdf_per_month != -1 else -1,
        }

        # 7. Response erstellen
        return SubscriptionStatusResponseDTO(
            subscription=SubscriptionResponseDTO(
                id=subscription.id,
                user_id=subscription.user_id,
                plan=subscription.plan,
                status=subscription.status,
                stripe_subscription_id=subscription.stripe_subscription_id,
                current_period_start=subscription.current_period_start,
                current_period_end=subscription.current_period_end,
                cancel_at_period_end=subscription.cancel_at_period_end
            ),
            limits=UsageLimitDTO(
                hook_per_month=plan_limits.hook_per_month,
                script_per_month=plan_limits.script_per_month,
                shotlist_per_month=plan_limits.shotlist_per_month,
                voiceover_per_month=plan_limits.voiceover_per_month,
                caption_per_month=plan_limits.caption_per_month,
                broll_per_month=plan_limits.broll_per_month,
                calendar_per_month=plan_limits.calendar_per_month,
                pdf_per_month=plan_limits.pdf_per_month
            ),
            current_usage=current_usage,
            remaining=remaining
        )
