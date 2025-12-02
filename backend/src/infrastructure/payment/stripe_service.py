import os
from typing import Optional, Dict, Any
import stripe
from datetime import datetime
from ...domain.entities.subscription import SubscriptionPlan, SubscriptionStatus


class StripeService:
    """
    Stripe Integration für Subscription Management.
    Handles Checkout, Customer Portal und Webhooks.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("STRIPE_SECRET_KEY")
        stripe.api_key = self.api_key

        # Price IDs für die Subscription Plans
        # Diese müssen in Stripe Dashboard erstellt werden
        self.price_ids = {
            SubscriptionPlan.BASIC: os.getenv("STRIPE_BASIC_PRICE_ID"),
            SubscriptionPlan.PRO: os.getenv("STRIPE_PRO_PRICE_ID"),
            SubscriptionPlan.ENTERPRISE: os.getenv("STRIPE_ENTERPRISE_PRICE_ID"),
        }

    async def create_checkout_session(
        self,
        user_id: str,
        user_email: str,
        plan: SubscriptionPlan,
        success_url: str,
        cancel_url: str
    ) -> str:
        """
        Erstellt eine Stripe Checkout Session für Subscription.

        Returns:
            checkout_url: URL zur Stripe Checkout Page
        """
        if plan == SubscriptionPlan.FREE:
            raise ValueError("FREE Plan benötigt keine Checkout Session")

        price_id = self.price_ids.get(plan)
        if not price_id:
            raise ValueError(f"Keine Price ID konfiguriert für Plan: {plan.value}")

        try:
            # Prüfe ob Customer bereits existiert
            customers = stripe.Customer.list(email=user_email, limit=1)

            if customers.data:
                customer_id = customers.data[0].id
            else:
                # Erstelle neuen Customer
                customer = stripe.Customer.create(
                    email=user_email,
                    metadata={"user_id": user_id}
                )
                customer_id = customer.id

            # Erstelle Checkout Session
            session = stripe.checkout.Session.create(
                customer=customer_id,
                mode="subscription",
                payment_method_types=["card"],
                line_items=[{
                    "price": price_id,
                    "quantity": 1,
                }],
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    "user_id": user_id,
                    "plan": plan.value
                },
                subscription_data={
                    "metadata": {
                        "user_id": user_id,
                        "plan": plan.value
                    }
                }
            )

            return session.url

        except stripe.error.StripeError as e:
            raise Exception(f"Stripe Checkout Fehler: {str(e)}")

    async def create_portal_session(
        self,
        stripe_customer_id: str,
        return_url: str
    ) -> str:
        """
        Erstellt eine Customer Portal Session für Subscription Management.
        User können hier ihre Subscription verwalten, kündigen, etc.

        Returns:
            portal_url: URL zum Stripe Customer Portal
        """
        try:
            session = stripe.billing_portal.Session.create(
                customer=stripe_customer_id,
                return_url=return_url,
            )
            return session.url

        except stripe.error.StripeError as e:
            raise Exception(f"Stripe Portal Fehler: {str(e)}")

    async def handle_webhook(
        self,
        payload: bytes,
        signature: str
    ) -> Dict[str, Any]:
        """
        Verarbeitet Stripe Webhook Events.

        Wichtige Events:
        - customer.subscription.created
        - customer.subscription.updated
        - customer.subscription.deleted
        - invoice.paid
        - invoice.payment_failed

        Returns:
            event_data: Extrahierte Daten für Application Layer
        """
        webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

        try:
            event = stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )
        except ValueError:
            raise Exception("Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise Exception("Invalid signature")

        event_type = event["type"]
        data = event["data"]["object"]

        # Process verschiedene Event Types
        if event_type == "customer.subscription.created":
            return await self._handle_subscription_created(data)

        elif event_type == "customer.subscription.updated":
            return await self._handle_subscription_updated(data)

        elif event_type == "customer.subscription.deleted":
            return await self._handle_subscription_deleted(data)

        elif event_type == "invoice.paid":
            return await self._handle_invoice_paid(data)

        elif event_type == "invoice.payment_failed":
            return await self._handle_payment_failed(data)

        else:
            # Unbekannter Event Type - einfach ignorieren
            return {
                "event_type": event_type,
                "handled": False
            }

    async def _handle_subscription_created(self, subscription: Dict) -> Dict[str, Any]:
        """Verarbeitet subscription.created Event"""
        user_id = subscription["metadata"].get("user_id")
        plan = subscription["metadata"].get("plan")

        return {
            "event_type": "subscription.created",
            "user_id": user_id,
            "stripe_subscription_id": subscription["id"],
            "stripe_customer_id": subscription["customer"],
            "plan": plan,
            "status": self._map_stripe_status(subscription["status"]),
            "current_period_start": datetime.fromtimestamp(subscription["current_period_start"]),
            "current_period_end": datetime.fromtimestamp(subscription["current_period_end"]),
            "cancel_at_period_end": subscription.get("cancel_at_period_end", False)
        }

    async def _handle_subscription_updated(self, subscription: Dict) -> Dict[str, Any]:
        """Verarbeitet subscription.updated Event"""
        user_id = subscription["metadata"].get("user_id")
        plan = subscription["metadata"].get("plan")

        return {
            "event_type": "subscription.updated",
            "user_id": user_id,
            "stripe_subscription_id": subscription["id"],
            "plan": plan,
            "status": self._map_stripe_status(subscription["status"]),
            "current_period_start": datetime.fromtimestamp(subscription["current_period_start"]),
            "current_period_end": datetime.fromtimestamp(subscription["current_period_end"]),
            "cancel_at_period_end": subscription.get("cancel_at_period_end", False)
        }

    async def _handle_subscription_deleted(self, subscription: Dict) -> Dict[str, Any]:
        """Verarbeitet subscription.deleted Event"""
        return {
            "event_type": "subscription.deleted",
            "stripe_subscription_id": subscription["id"],
            "status": SubscriptionStatus.CANCELED.value
        }

    async def _handle_invoice_paid(self, invoice: Dict) -> Dict[str, Any]:
        """Verarbeitet invoice.paid Event"""
        subscription_id = invoice.get("subscription")

        return {
            "event_type": "invoice.paid",
            "stripe_subscription_id": subscription_id,
            "amount_paid": invoice["amount_paid"],
            "currency": invoice["currency"],
            "invoice_id": invoice["id"]
        }

    async def _handle_payment_failed(self, invoice: Dict) -> Dict[str, Any]:
        """Verarbeitet invoice.payment_failed Event"""
        subscription_id = invoice.get("subscription")

        return {
            "event_type": "invoice.payment_failed",
            "stripe_subscription_id": subscription_id,
            "amount_due": invoice["amount_due"],
            "invoice_id": invoice["id"],
            "status": SubscriptionStatus.PAST_DUE.value
        }

    def _map_stripe_status(self, stripe_status: str) -> str:
        """Mappt Stripe Status zu unseren SubscriptionStatus Enum Values"""
        status_map = {
            "active": SubscriptionStatus.ACTIVE.value,
            "canceled": SubscriptionStatus.CANCELED.value,
            "past_due": SubscriptionStatus.PAST_DUE.value,
            "trialing": SubscriptionStatus.TRIALING.value,
            "incomplete": SubscriptionStatus.PAST_DUE.value,
            "incomplete_expired": SubscriptionStatus.CANCELED.value,
            "unpaid": SubscriptionStatus.PAST_DUE.value,
        }
        return status_map.get(stripe_status, SubscriptionStatus.CANCELED.value)

    async def get_subscription(self, stripe_subscription_id: str) -> Dict[str, Any]:
        """
        Holt Subscription Details von Stripe.
        Nützlich für Sync zwischen Stripe und unserer DB.
        """
        try:
            subscription = stripe.Subscription.retrieve(stripe_subscription_id)

            return {
                "id": subscription["id"],
                "customer": subscription["customer"],
                "status": self._map_stripe_status(subscription["status"]),
                "current_period_start": datetime.fromtimestamp(subscription["current_period_start"]),
                "current_period_end": datetime.fromtimestamp(subscription["current_period_end"]),
                "cancel_at_period_end": subscription.get("cancel_at_period_end", False),
                "plan": subscription["metadata"].get("plan", "basic")
            }

        except stripe.error.StripeError as e:
            raise Exception(f"Fehler beim Abrufen der Subscription: {str(e)}")

    async def cancel_subscription(
        self,
        stripe_subscription_id: str,
        immediately: bool = False
    ) -> Dict[str, Any]:
        """
        Kündigt eine Subscription.

        Args:
            stripe_subscription_id: Stripe Subscription ID
            immediately: Wenn True, sofort kündigen. Wenn False, am Period-Ende.
        """
        try:
            if immediately:
                subscription = stripe.Subscription.delete(stripe_subscription_id)
            else:
                subscription = stripe.Subscription.modify(
                    stripe_subscription_id,
                    cancel_at_period_end=True
                )

            return {
                "subscription_id": subscription["id"],
                "status": self._map_stripe_status(subscription["status"]),
                "cancel_at_period_end": subscription.get("cancel_at_period_end", False),
                "canceled_at": datetime.fromtimestamp(subscription["canceled_at"]) if subscription.get("canceled_at") else None
            }

        except stripe.error.StripeError as e:
            raise Exception(f"Fehler beim Kündigen der Subscription: {str(e)}")
