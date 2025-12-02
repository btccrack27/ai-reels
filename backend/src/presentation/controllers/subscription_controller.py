from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from ...application.dto.subscription_dto import (
    CreateCheckoutSessionRequestDTO,
    CreatePortalSessionRequestDTO,
    WebhookEventDTO,
    CheckoutSessionResponseDTO,
    PortalSessionResponseDTO,
    SubscriptionStatusResponseDTO,
    WebhookEventResponseDTO
)
from ...domain.entities.subscription import SubscriptionPlan
from ...application.use_cases.create_checkout_session_use_case import CreateCheckoutSessionUseCase
from ...application.use_cases.create_portal_session_use_case import CreatePortalSessionUseCase
from ...application.use_cases.handle_subscription_webhook_use_case import HandleSubscriptionWebhookUseCase
from ...application.use_cases.get_subscription_status_use_case import GetSubscriptionStatusUseCase
from ..middlewares import get_current_user
from ..dependencies import (
    get_create_checkout_session_use_case,
    get_create_portal_session_use_case,
    get_handle_subscription_webhook_use_case,
    get_get_subscription_status_use_case
)


router = APIRouter(prefix="/api/subscription", tags=["subscription"])


# ============== Request Models ==============

class CheckoutRequest(BaseModel):
    plan: str  # "basic", "pro", "enterprise"
    success_url: str
    cancel_url: str


class PortalRequest(BaseModel):
    return_url: str


# ============== Endpoints ==============

@router.post("/checkout", response_model=CheckoutSessionResponseDTO)
async def create_checkout_session(
    request: CheckoutRequest,
    current_user: dict = Depends(get_current_user),
    use_case: CreateCheckoutSessionUseCase = Depends(get_create_checkout_session_use_case)
):
    """
    Erstellt Stripe Checkout Session für Plan-Upgrade.

    Plans: basic, pro, enterprise

    Requires: Authentication

    Returns:
    - checkout_url: URL zur Stripe Checkout Page

    Errors:
    - 400: Invalid plan oder User hat keine Stripe Customer ID
    - 500: Stripe Error
    """
    try:
        # Plan String → Enum
        plan_map = {
            "basic": SubscriptionPlan.BASIC,
            "pro": SubscriptionPlan.PRO,
            "enterprise": SubscriptionPlan.ENTERPRISE
        }
        plan = plan_map.get(request.plan.lower())
        if not plan:
            raise ValueError(f"Invalid plan: {request.plan}")

        dto = CreateCheckoutSessionRequestDTO(
            user_id=current_user["user_id"],
            plan=plan,
            success_url=request.success_url,
            cancel_url=request.cancel_url
        )
        result = await use_case.execute(dto)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler beim Erstellen der Checkout Session: {str(e)}"
        )


@router.post("/portal", response_model=PortalSessionResponseDTO)
async def create_portal_session(
    request: PortalRequest,
    current_user: dict = Depends(get_current_user),
    use_case: CreatePortalSessionUseCase = Depends(get_create_portal_session_use_case)
):
    """
    Erstellt Stripe Customer Portal Session.

    User können hier:
    - Subscription upgraden/downgraden
    - Zahlungsmethode ändern
    - Subscription kündigen
    - Rechnungen ansehen

    Requires: Authentication

    Returns:
    - portal_url: URL zum Stripe Customer Portal

    Errors:
    - 400: User hat noch keine Stripe Subscription
    - 500: Stripe Error
    """
    try:
        dto = CreatePortalSessionRequestDTO(
            user_id=current_user["user_id"],
            return_url=request.return_url
        )
        result = await use_case.execute(dto)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler beim Erstellen der Portal Session: {str(e)}"
        )


@router.post("/webhook", response_model=WebhookEventResponseDTO)
async def handle_stripe_webhook(
    request: Request,
    use_case: HandleSubscriptionWebhookUseCase = Depends(get_handle_subscription_webhook_use_case)
):
    """
    Stripe Webhook Endpoint.

    Handled Events:
    - customer.subscription.created
    - customer.subscription.updated
    - customer.subscription.deleted
    - invoice.paid
    - invoice.payment_failed

    WICHTIG: Dieser Endpoint ist öffentlich (keine Authentication)!
    Security durch Stripe Webhook Signature Verification.

    Returns:
    - event_type: Typ des Events
    - processed: Ob Event erfolgreich verarbeitet
    - message: Status Message

    Errors:
    - 400: Invalid signature oder Event
    - 500: Processing Error
    """
    try:
        # Raw body für Signature Verification
        payload = await request.body()
        signature = request.headers.get("stripe-signature")

        if not signature:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing stripe-signature header"
            )

        dto = WebhookEventDTO(
            payload=payload,
            signature=signature
        )
        result = await use_case.execute(dto)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler beim Verarbeiten des Webhooks: {str(e)}"
        )


@router.get("/status", response_model=SubscriptionStatusResponseDTO)
async def get_subscription_status(
    current_user: dict = Depends(get_current_user),
    use_case: GetSubscriptionStatusUseCase = Depends(get_get_subscription_status_use_case)
):
    """
    Gibt vollständigen Subscription Status zurück.

    Requires: Authentication

    Returns:
    - subscription: Details (Plan, Status, Billing Dates)
    - limits: Plan Limits für alle Content Types
    - current_usage: Aktuelle Usage diesen Monat
    - remaining: Verbleibende Quota

    Errors:
    - 401: Not authenticated
    - 404: User oder Subscription nicht gefunden
    - 500: Server Error
    """
    try:
        result = await use_case.execute(current_user["user_id"])
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler beim Laden des Subscription Status: {str(e)}"
        )
