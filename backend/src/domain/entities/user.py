from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    """User-Rollen basierend auf Subscription-Plan"""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"


@dataclass
class User:
    """
    User Entity.
    Repräsentiert einen registrierten User mit Subscription.
    """
    id: str
    email: str
    name: str
    role: UserRole
    password_hash: str = None
    subscription_id: Optional[str] = None
    stripe_customer_id: Optional[str] = None
    created_at: datetime = None
    updated_at: datetime = None
    is_active: bool = True

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
