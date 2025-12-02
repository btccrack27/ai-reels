from datetime import datetime
from ...domain.interfaces.user_repository import IUserRepository
from ...domain.interfaces.subscription_repository import ISubscriptionRepository
from ...domain.entities.subscription import Subscription, SubscriptionPlan, SubscriptionStatus
from ...domain.entities.user import UserRole
from ...infrastructure.payment.stripe_service import StripeService
from ..dto.subscription_dto import WebhookEventDTO, WebhookEventResponseDTO
import uuid


class HandleSubscriptionWebhookUseCase:
    """
    Use Case für Stripe Webhook Event Handling.

    Flow:
    1. Webhook Signature verifizieren
    2. Event Type identifizieren
    3. Entsprechende Action ausführen:
       - subscription.created → Subscription erstellen
       - subscription.updated → Subscription updaten
       - subscription.deleted → Subscription kündigen
       - invoice.paid → Status auf active setzen
       - invoice.payment_failed → Status auf past_due setzen
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        subscription_repository: ISubscriptionRepository,
        stripe_service: StripeService
    ):
        self.user_repo = user_repository
        self.subscription_repo = subscription_repository
        self.stripe_service = stripe_service

    async def execute(self, request: WebhookEventDTO) -> WebhookEventResponseDTO:
        """
        Verarbeitet Stripe Webhook Event.

        Args:
            request: WebhookEventDTO mit payload, signature

        Returns:
            WebhookEventResponseDTO mit event_type, processed, message

        Raises:
            Exception: Bei Signature Verification Fehler
        """
        # 1. Webhook verarbeiten und Event Data extrahieren
        try:
            event_data = await self.stripe_service.handle_webhook(
                payload=request.payload,
                signature=request.signature
            )
        except Exception as e:
            raise Exception(f"Webhook Verification fehlgeschlagen: {str(e)}")

        event_type = event_data.get("event_type")

        # 2. Event Type handling
        if event_type == "subscription.created":
            await self._handle_subscription_created(event_data)
            message = "Subscription erstellt"

        elif event_type == "subscription.updated":
            await self._handle_subscription_updated(event_data)
            message = "Subscription aktualisiert"

        elif event_type == "subscription.deleted":
            await self._handle_subscription_deleted(event_data)
            message = "Subscription gekündigt"

        elif event_type == "invoice.paid":
            await self._handle_invoice_paid(event_data)
            message = "Zahlung erfolgreich"

        elif event_type == "invoice.payment_failed":
            await self._handle_payment_failed(event_data)
            message = "Zahlung fehlgeschlagen"

        else:
            message = f"Event Type {event_type} nicht handled"

        return WebhookEventResponseDTO(
            event_type=event_type,
            processed=True,
            message=message
        )

    async def _handle_subscription_created(self, event_data: dict):
        """Erstellt neue Subscription in DB"""
        user_id = event_data.get("user_id")
        stripe_subscription_id = event_data.get("stripe_subscription_id")
        stripe_customer_id = event_data.get("stripe_customer_id")
        plan_str = event_data.get("plan")
        status_str = event_data.get("status")

        # User laden und Stripe Customer ID setzen
        user = await self.user_repo.get_by_id(user_id)
        if user:
            await self.user_repo.update(
                user_id=user_id,
                stripe_customer_id=stripe_customer_id,
                role=UserRole(plan_str)
            )

        # Subscription erstellen
        subscription = Subscription(
            id=str(uuid.uuid4()),
            user_id=user_id,
            plan=SubscriptionPlan(plan_str),
            status=SubscriptionStatus(status_str),
            stripe_subscription_id=stripe_subscription_id,
            current_period_start=event_data.get("current_period_start"),
            current_period_end=event_data.get("current_period_end"),
            cancel_at_period_end=event_data.get("cancel_at_period_end", False)
        )

        created_subscription = await self.subscription_repo.create(subscription)

        # User mit subscription_id updaten
        await self.user_repo.update(
            user_id=user_id,
            subscription_id=created_subscription.id
        )

    async def _handle_subscription_updated(self, event_data: dict):
        """Updated existierende Subscription"""
        stripe_subscription_id = event_data.get("stripe_subscription_id")

        # Subscription per Stripe ID finden
        subscription = await self.subscription_repo.get_by_stripe_id(stripe_subscription_id)
        if not subscription:
            return  # Subscription noch nicht in DB

        # Subscription updaten
        plan_str = event_data.get("plan")
        status_str = event_data.get("status")

        await self.subscription_repo.update(
            subscription_id=subscription.id,
            plan=SubscriptionPlan(plan_str) if plan_str else subscription.plan,
            status=SubscriptionStatus(status_str),
            current_period_start=event_data.get("current_period_start"),
            current_period_end=event_data.get("current_period_end"),
            cancel_at_period_end=event_data.get("cancel_at_period_end", False)
        )

        # User Role updaten wenn Plan geändert
        if plan_str:
            await self.user_repo.update(
                user_id=subscription.user_id,
                role=UserRole(plan_str)
            )

    async def _handle_subscription_deleted(self, event_data: dict):
        """Kündigt Subscription (Status → canceled, User Role → free)"""
        stripe_subscription_id = event_data.get("stripe_subscription_id")

        subscription = await self.subscription_repo.get_by_stripe_id(stripe_subscription_id)
        if not subscription:
            return

        # Subscription Status → canceled
        await self.subscription_repo.update(
            subscription_id=subscription.id,
            status=SubscriptionStatus.CANCELED
        )

        # User Role → FREE
        await self.user_repo.update(
            user_id=subscription.user_id,
            role=UserRole.FREE
        )

    async def _handle_invoice_paid(self, event_data: dict):
        """Setzt Subscription Status auf active nach erfolgreicher Zahlung"""
        stripe_subscription_id = event_data.get("stripe_subscription_id")
        if not stripe_subscription_id:
            return

        subscription = await self.subscription_repo.get_by_stripe_id(stripe_subscription_id)
        if not subscription:
            return

        await self.subscription_repo.update(
            subscription_id=subscription.id,
            status=SubscriptionStatus.ACTIVE
        )

    async def _handle_payment_failed(self, event_data: dict):
        """Setzt Subscription Status auf past_due nach fehlgeschlagener Zahlung"""
        stripe_subscription_id = event_data.get("stripe_subscription_id")
        if not stripe_subscription_id:
            return

        subscription = await self.subscription_repo.get_by_stripe_id(stripe_subscription_id)
        if not subscription:
            return

        await self.subscription_repo.update(
            subscription_id=subscription.id,
            status=SubscriptionStatus.PAST_DUE
        )
