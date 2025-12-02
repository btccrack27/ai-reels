from dataclasses import dataclass
from datetime import datetime


@dataclass
class Usage:
    """
    Usage Entity.
    Trackt die Content-Generierung pro User für Rate-Limiting.
    """
    id: str
    user_id: str
    content_type: str  # hook, script, shotlist, etc.
    count: int
    period_start: datetime
    period_end: datetime

    def has_exceeded_limit(self, limit: int) -> bool:
        """
        Prüft ob das Limit überschritten wurde.

        Args:
            limit: Das Limit für diesen Content-Typ (-1 = unlimited)

        Returns:
            True wenn Limit überschritten, False sonst
        """
        if limit == -1:  # Unlimited
            return False
        return self.count >= limit

    def increment(self) -> None:
        """Erhöht den Usage-Counter um 1"""
        self.count += 1

    def is_current_period(self, now: datetime = None) -> bool:
        """Prüft ob die Usage-Period noch aktiv ist"""
        if now is None:
            now = datetime.utcnow()
        return self.period_start <= now <= self.period_end
