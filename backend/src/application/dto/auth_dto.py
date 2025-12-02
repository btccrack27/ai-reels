from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from ...domain.entities.user import UserRole


# ================== Request DTOs ==================

@dataclass
class RegisterRequestDTO:
    """DTO für User-Registrierung"""
    email: str
    name: str
    password: str


@dataclass
class LoginRequestDTO:
    """DTO für User-Login"""
    email: str
    password: str


@dataclass
class RefreshTokenRequestDTO:
    """DTO für Token-Refresh"""
    refresh_token: str


# ================== Response DTOs ==================

@dataclass
class UserResponseDTO:
    """DTO für User-Informationen"""
    id: str
    email: str
    name: str
    role: UserRole
    subscription_id: Optional[str]
    stripe_customer_id: Optional[str]
    is_active: bool
    created_at: datetime


@dataclass
class AuthTokensDTO:
    """DTO für Authentication Tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 3600  # 1 Stunde


@dataclass
class LoginResponseDTO:
    """DTO für Login Response"""
    user: UserResponseDTO
    tokens: AuthTokensDTO


@dataclass
class RegisterResponseDTO:
    """DTO für Register Response"""
    user: UserResponseDTO
    tokens: AuthTokensDTO


@dataclass
class RefreshTokenResponseDTO:
    """DTO für Token Refresh Response"""
    tokens: AuthTokensDTO
