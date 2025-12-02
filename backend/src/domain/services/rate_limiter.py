from ..entities.subscription import Subscription, PLAN_LIMITS
from ..entities.usage import Usage
from ..entities.content import ContentType


class RateLimiter:
    """
    Domain Service für Rate-Limiting.
    Prüft ob ein User basierend auf seinem Plan Content generieren darf.
    """

    def can_generate(
        self,
        subscription: Subscription,
        content_type: ContentType,
        current_usage: Usage
    ) -> tuple[bool, str]:
        """
        Prüft ob User Content generieren darf.

        Args:
            subscription: User's Subscription
            content_type: Typ des zu generierenden Contents
            current_usage: Aktuelle Usage für diesen Content-Typ

        Returns:
            (can_generate: bool, error_message: str)
        """
        if not subscription.is_active():
            return False, "Subscription ist nicht aktiv"

        limits = PLAN_LIMITS[subscription.plan]

        # Mapping Content-Type zu Limit
        limit_map = {
            ContentType.HOOK: limits.hook_per_month,
            ContentType.SCRIPT: limits.script_per_month,
            ContentType.SHOTLIST: limits.shotlist_per_month,
            ContentType.VOICEOVER: limits.voiceover_per_month,
            ContentType.CAPTION: limits.caption_per_month,
            ContentType.BROLL: limits.broll_per_month,
            ContentType.CALENDAR: limits.calendar_per_month,
        }

        content_limit = limit_map.get(content_type)
        if content_limit is None:
            return False, f"Unbekannter Content-Typ: {content_type}"

        # Unlimited check
        if content_limit == -1:
            return True, ""

        # Check if limit exceeded
        if current_usage.has_exceeded_limit(content_limit):
            remaining = 0
        else:
            remaining = content_limit - current_usage.count

        if remaining <= 0:
            return False, (
                f"Monatliches Limit für {content_type.value} erreicht. "
                f"Upgrade deinen Plan für mehr Content."
            )

        return True, ""

    def can_export_pdf(
        self,
        subscription: Subscription,
        current_usage: Usage
    ) -> tuple[bool, str]:
        """
        Prüft ob User PDF exportieren darf.

        Args:
            subscription: User's Subscription
            current_usage: Aktuelle PDF-Export Usage

        Returns:
            (can_export: bool, error_message: str)
        """
        if not subscription.is_active():
            return False, "Subscription ist nicht aktiv"

        limits = PLAN_LIMITS[subscription.plan]
        pdf_limit = limits.pdf_exports_per_month

        # Unlimited check
        if pdf_limit == -1:
            return True, ""

        # Check if limit exceeded
        if current_usage.has_exceeded_limit(pdf_limit):
            return False, (
                "Monatliches PDF-Export Limit erreicht. "
                "Upgrade deinen Plan für mehr Exports."
            )

        return True, ""

    def get_remaining_usage(
        self,
        subscription: Subscription,
        content_type: ContentType,
        current_usage: Usage
    ) -> int:
        """
        Gibt die verbleibende Anzahl an Generierungen zurück.

        Returns:
            -1 für unlimited, sonst die verbleibende Anzahl
        """
        limits = PLAN_LIMITS[subscription.plan]

        limit_map = {
            ContentType.HOOK: limits.hook_per_month,
            ContentType.SCRIPT: limits.script_per_month,
            ContentType.SHOTLIST: limits.shotlist_per_month,
            ContentType.VOICEOVER: limits.voiceover_per_month,
            ContentType.CAPTION: limits.caption_per_month,
            ContentType.BROLL: limits.broll_per_month,
            ContentType.CALENDAR: limits.calendar_per_month,
        }

        content_limit = limit_map.get(content_type)
        if content_limit == -1:
            return -1

        remaining = content_limit - current_usage.count
        return max(0, remaining)
