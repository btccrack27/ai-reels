from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class SubscriptionPlan(str, Enum):
    """Subscription Plan Tiers"""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, Enum):
    """Status einer Subscription"""
    ACTIVE = "active"
    CANCELED = "canceled"
    PAST_DUE = "past_due"
    TRIALING = "trialing"


@dataclass
class PlanLimits:
    """Usage-Limits pro Subscription-Plan"""
    hook_per_month: int
    script_per_month: int
    shotlist_per_month: int
    voiceover_per_month: int
    caption_per_month: int
    broll_per_month: int
    calendar_per_month: int
    pdf_exports_per_month: int


# Plan-Konfiguration
PLAN_LIMITS = {
    SubscriptionPlan.FREE: PlanLimits(
        hook_per_month=5,
        script_per_month=3,
        shotlist_per_month=3,
        voiceover_per_month=3,
        caption_per_month=5,
        broll_per_month=3,
        calendar_per_month=1,
        pdf_exports_per_month=2
    ),
    SubscriptionPlan.BASIC: PlanLimits(
        hook_per_month=50,
        script_per_month=30,
        shotlist_per_month=30,
        voiceover_per_month=30,
        caption_per_month=50,
        broll_per_month=30,
        calendar_per_month=5,
        pdf_exports_per_month=20
    ),
    SubscriptionPlan.PRO: PlanLimits(
        hook_per_month=500,
        script_per_month=300,
        shotlist_per_month=300,
        voiceover_per_month=300,
        caption_per_month=500,
        broll_per_month=300,
        calendar_per_month=20,
        pdf_exports_per_month=200
    ),
    SubscriptionPlan.ENTERPRISE: PlanLimits(
        hook_per_month=-1,  # Unlimited
        script_per_month=-1,
        shotlist_per_month=-1,
        voiceover_per_month=-1,
        caption_per_month=-1,
        broll_per_month=-1,
        calendar_per_month=-1,
        pdf_exports_per_month=-1
    )
}


@dataclass
class Subscription:
    """
    Subscription Entity.
    Verwaltet den Subscription-Status eines Users.
    """
    id: str
    user_id: str
    plan: SubscriptionPlan
    status: SubscriptionStatus
    stripe_subscription_id: Optional[str]
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool = False

    def get_limits(self) -> PlanLimits:
        """Gibt die Limits für den aktuellen Plan zurück"""
        return PLAN_LIMITS[self.plan]

    def is_active(self) -> bool:
        """Prüft ob die Subscription aktiv ist"""
        return self.status in [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING]
