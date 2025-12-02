from ...domain.interfaces.user_repository import IUserRepository
from ...domain.entities.subscription import SubscriptionPlan
from ...infrastructure.payment.stripe_service import StripeService
from ..dto.subscription_dto import CreateCheckoutSessionRequestDTO, CheckoutSessionResponseDTO


class CreateCheckoutSessionUseCase:
    """
    Use Case für Stripe Checkout Session Erstellung.

    Flow:
    1. User laden
    2. Stripe Checkout Session erstellen
    3. Checkout URL zurückgeben
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        stripe_service: StripeService
    ):
        self.user_repo = user_repository
        self.stripe_service = stripe_service

    async def execute(self, request: CreateCheckoutSessionRequestDTO) -> CheckoutSessionResponseDTO:
        """
        Erstellt Stripe Checkout Session für Plan-Upgrade.

        Args:
            request: CreateCheckoutSessionRequestDTO mit user_id, plan, URLs

        Returns:
            CheckoutSessionResponseDTO mit checkout_url

        Raises:
            ValueError: Wenn User nicht existiert oder Plan FREE ist
        """
        # 1. User laden
        user = await self.user_repo.get_by_id(request.user_id)
        if not user:
            raise ValueError(f"User {request.user_id} nicht gefunden")

        # 2. Validierung
        if request.plan == SubscriptionPlan.FREE:
            raise ValueError("FREE Plan benötigt keine Checkout Session")

        # 3. Stripe Checkout Session erstellen
        try:
            checkout_url = await self.stripe_service.create_checkout_session(
                user_id=request.user_id,
                user_email=user.email,
                plan=request.plan,
                success_url=request.success_url,
                cancel_url=request.cancel_url
            )
        except Exception as e:
            raise Exception(f"Fehler beim Erstellen der Checkout Session: {str(e)}")

        # 4. Response zurückgeben
        return CheckoutSessionResponseDTO(
            checkout_url=checkout_url
        )
