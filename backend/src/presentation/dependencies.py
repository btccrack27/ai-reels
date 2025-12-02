"""
Dependency Injection Setup für FastAPI.
Erstellt Use Cases mit ihren Dependencies (Repositories, Services).
"""
from functools import lru_cache
from ..infrastructure.database.postgres.config import async_session_maker
from ..infrastructure.database.postgres.content_repository import PostgresContentRepository
from ..infrastructure.database.postgres.user_repository import PostgresUserRepository
from ..infrastructure.database.postgres.subscription_repository import PostgresSubscriptionRepository
from ..infrastructure.database.postgres.usage_repository import PostgresUsageRepository
from ..infrastructure.ai_services.claude_service import ClaudeService
from ..infrastructure.payment.stripe_service import StripeService
from ..infrastructure.pdf.pdf_generator import PDFGenerator
from ..domain.services.rate_limiter import RateLimiter
from ..domain.services.content_validator import ContentValidator

# Application Layer
from ..application.use_cases.generate_hook_use_case import GenerateHookUseCase
from ..application.use_cases.generate_script_use_case import GenerateScriptUseCase
from ..application.use_cases.generate_shotlist_use_case import GenerateShotlistUseCase
from ..application.use_cases.generate_voiceover_use_case import GenerateVoiceoverUseCase
from ..application.use_cases.generate_caption_use_case import GenerateCaptionUseCase
from ..application.use_cases.generate_broll_use_case import GenerateBRollUseCase
from ..application.use_cases.generate_calendar_use_case import GenerateCalendarUseCase
from ..application.use_cases.register_user_use_case import RegisterUserUseCase
from ..application.use_cases.login_user_use_case import LoginUserUseCase
from ..application.use_cases.create_checkout_session_use_case import CreateCheckoutSessionUseCase
from ..application.use_cases.create_portal_session_use_case import CreatePortalSessionUseCase
from ..application.use_cases.handle_subscription_webhook_use_case import HandleSubscriptionWebhookUseCase
from ..application.use_cases.get_subscription_status_use_case import GetSubscriptionStatusUseCase
from ..application.use_cases.export_pdf_use_case import ExportPDFUseCase


# ============== Shared Services (Singleton) ==============

@lru_cache()
def get_claude_service() -> ClaudeService:
    """Claude Service Singleton"""
    return ClaudeService()


@lru_cache()
def get_stripe_service() -> StripeService:
    """Stripe Service Singleton"""
    return StripeService()


@lru_cache()
def get_pdf_generator() -> PDFGenerator:
    """PDF Generator Singleton"""
    return PDFGenerator()


@lru_cache()
def get_rate_limiter() -> RateLimiter:
    """Rate Limiter Service Singleton"""
    return RateLimiter()


@lru_cache()
def get_content_validator() -> ContentValidator:
    """Content Validator Service Singleton"""
    return ContentValidator()


# ============== Database Session ==============

async def get_session():
    """Provides async database session"""
    async with async_session_maker() as session:
        yield session


# ============== Use Case Dependencies ==============

# Content Generation Use Cases

async def get_generate_hook_use_case():
    """Dependency for GenerateHookUseCase"""
    async with async_session_maker() as session:
        return GenerateHookUseCase(
            content_repository=PostgresContentRepository(session),
            user_repository=PostgresUserRepository(session),
            subscription_repository=PostgresSubscriptionRepository(session),
            usage_repository=PostgresUsageRepository(session),
            claude_service=get_claude_service(),
            rate_limiter=get_rate_limiter(),
            content_validator=get_content_validator()
        )


async def get_generate_script_use_case():
    """Dependency for GenerateScriptUseCase"""
    async with async_session_maker() as session:
        return GenerateScriptUseCase(
            content_repository=PostgresContentRepository(session),
            user_repository=PostgresUserRepository(session),
            subscription_repository=PostgresSubscriptionRepository(session),
            usage_repository=PostgresUsageRepository(session),
            claude_service=get_claude_service(),
            rate_limiter=get_rate_limiter(),
            content_validator=get_content_validator()
        )


async def get_generate_shotlist_use_case():
    """Dependency for GenerateShotlistUseCase"""
    async with async_session_maker() as session:
        return GenerateShotlistUseCase(
            content_repository=PostgresContentRepository(session),
            user_repository=PostgresUserRepository(session),
            subscription_repository=PostgresSubscriptionRepository(session),
            usage_repository=PostgresUsageRepository(session),
            claude_service=get_claude_service(),
            rate_limiter=get_rate_limiter(),
            content_validator=get_content_validator()
        )


async def get_generate_voiceover_use_case():
    """Dependency for GenerateVoiceoverUseCase"""
    async with async_session_maker() as session:
        return GenerateVoiceoverUseCase(
            content_repository=PostgresContentRepository(session),
            user_repository=PostgresUserRepository(session),
            subscription_repository=PostgresSubscriptionRepository(session),
            usage_repository=PostgresUsageRepository(session),
            claude_service=get_claude_service(),
            rate_limiter=get_rate_limiter(),
            content_validator=get_content_validator()
        )


async def get_generate_caption_use_case():
    """Dependency for GenerateCaptionUseCase"""
    async with async_session_maker() as session:
        return GenerateCaptionUseCase(
            content_repository=PostgresContentRepository(session),
            user_repository=PostgresUserRepository(session),
            subscription_repository=PostgresSubscriptionRepository(session),
            usage_repository=PostgresUsageRepository(session),
            claude_service=get_claude_service(),
            rate_limiter=get_rate_limiter(),
            content_validator=get_content_validator()
        )


async def get_generate_broll_use_case():
    """Dependency for GenerateBRollUseCase"""
    async with async_session_maker() as session:
        return GenerateBRollUseCase(
            content_repository=PostgresContentRepository(session),
            user_repository=PostgresUserRepository(session),
            subscription_repository=PostgresSubscriptionRepository(session),
            usage_repository=PostgresUsageRepository(session),
            claude_service=get_claude_service(),
            rate_limiter=get_rate_limiter(),
            content_validator=get_content_validator()
        )


async def get_generate_calendar_use_case():
    """Dependency for GenerateCalendarUseCase"""
    async with async_session_maker() as session:
        return GenerateCalendarUseCase(
            content_repository=PostgresContentRepository(session),
            user_repository=PostgresUserRepository(session),
            subscription_repository=PostgresSubscriptionRepository(session),
            usage_repository=PostgresUsageRepository(session),
            claude_service=get_claude_service(),
            rate_limiter=get_rate_limiter(),
            content_validator=get_content_validator()
        )


# Authentication Use Cases

async def get_register_user_use_case():
    """Dependency for RegisterUserUseCase"""
    async with async_session_maker() as session:
        return RegisterUserUseCase(
            user_repository=PostgresUserRepository(session),
            subscription_repository=PostgresSubscriptionRepository(session)
        )


async def get_login_user_use_case():
    """Dependency for LoginUserUseCase"""
    async with async_session_maker() as session:
        return LoginUserUseCase(
            user_repository=PostgresUserRepository(session)
        )


# Subscription Use Cases

async def get_create_checkout_session_use_case():
    """Dependency for CreateCheckoutSessionUseCase"""
    async with async_session_maker() as session:
        return CreateCheckoutSessionUseCase(
            user_repository=PostgresUserRepository(session),
            stripe_service=get_stripe_service()
        )


async def get_create_portal_session_use_case():
    """Dependency for CreatePortalSessionUseCase"""
    async with async_session_maker() as session:
        return CreatePortalSessionUseCase(
            user_repository=PostgresUserRepository(session),
            stripe_service=get_stripe_service()
        )


async def get_handle_subscription_webhook_use_case():
    """Dependency for HandleSubscriptionWebhookUseCase"""
    async with async_session_maker() as session:
        return HandleSubscriptionWebhookUseCase(
            user_repository=PostgresUserRepository(session),
            subscription_repository=PostgresSubscriptionRepository(session),
            stripe_service=get_stripe_service()
        )


async def get_get_subscription_status_use_case():
    """Dependency for GetSubscriptionStatusUseCase"""
    async with async_session_maker() as session:
        return GetSubscriptionStatusUseCase(
            user_repository=PostgresUserRepository(session),
            subscription_repository=PostgresSubscriptionRepository(session),
            usage_repository=PostgresUsageRepository(session)
        )


# Export Use Cases

async def get_export_pdf_use_case():
    """Dependency for ExportPDFUseCase"""
    async with async_session_maker() as session:
        return ExportPDFUseCase(
            content_repository=PostgresContentRepository(session),
            user_repository=PostgresUserRepository(session),
            subscription_repository=PostgresSubscriptionRepository(session),
            usage_repository=PostgresUsageRepository(session),
            pdf_generator=get_pdf_generator(),
            rate_limiter=get_rate_limiter()
        )
