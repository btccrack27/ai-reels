from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime
from ...domain.entities.subscription import SubscriptionPlan, SubscriptionStatus


# ================== Request DTOs ==================

@dataclass
class CreateCheckoutSessionRequestDTO:
    """DTO für Stripe Checkout Session Erstellung"""
    user_id: str
    plan: SubscriptionPlan
    success_url: str
    cancel_url: str


@dataclass
class CreatePortalSessionRequestDTO:
    """DTO für Stripe Customer Portal Session Erstellung"""
    user_id: str
    return_url: str


@dataclass
class WebhookEventDTO:
    """DTO für Stripe Webhook Events"""
    payload: bytes
    signature: str


@dataclass
class CancelSubscriptionRequestDTO:
    """DTO für Subscription-Kündigung"""
    user_id: str
    immediately: bool = False  # Wenn False, am Period-Ende kündigen


# ================== Response DTOs ==================

@dataclass
class SubscriptionResponseDTO:
    """DTO für Subscription-Informationen"""
    id: str
    user_id: str
    plan: SubscriptionPlan
    status: SubscriptionStatus
    stripe_subscription_id: Optional[str]
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool


@dataclass
class CheckoutSessionResponseDTO:
    """DTO für Checkout Session Response"""
    checkout_url: str
    session_id: Optional[str] = None


@dataclass
class PortalSessionResponseDTO:
    """DTO für Portal Session Response"""
    portal_url: str


@dataclass
class UsageLimitDTO:
    """DTO für Usage-Limits eines Plans"""
    hook_per_month: int
    script_per_month: int
    shotlist_per_month: int
    voiceover_per_month: int
    caption_per_month: int
    broll_per_month: int
    calendar_per_month: int
    pdf_per_month: int


@dataclass
class CurrentUsageDTO:
    """DTO für aktuelle Usage"""
    hook: int
    script: int
    shotlist: int
    voiceover: int
    caption: int
    broll: int
    calendar: int
    pdf: int


@dataclass
class SubscriptionStatusResponseDTO:
    """DTO für vollständige Subscription Status Informationen"""
    subscription: SubscriptionResponseDTO
    limits: UsageLimitDTO
    current_usage: CurrentUsageDTO
    remaining: Dict[str, int]  # Map von content_type → verbleibende Anzahl


@dataclass
class WebhookEventResponseDTO:
    """DTO für Webhook Event Processing Response"""
    event_type: str
    processed: bool
    message: str
