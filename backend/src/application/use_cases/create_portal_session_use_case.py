from ...domain.interfaces.user_repository import IUserRepository
from ...infrastructure.payment.stripe_service import StripeService
from ..dto.subscription_dto import CreatePortalSessionRequestDTO, PortalSessionResponseDTO


class CreatePortalSessionUseCase:
    """
    Use Case für Stripe Customer Portal Session Erstellung.

    Flow:
    1. User laden
    2. Stripe Customer ID prüfen
    3. Portal Session erstellen
    4. Portal URL zurückgeben
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        stripe_service: StripeService
    ):
        self.user_repo = user_repository
        self.stripe_service = stripe_service

    async def execute(self, request: CreatePortalSessionRequestDTO) -> PortalSessionResponseDTO:
        """
        Erstellt Stripe Customer Portal Session.

        Args:
            request: CreatePortalSessionRequestDTO mit user_id, return_url

        Returns:
            PortalSessionResponseDTO mit portal_url

        Raises:
            ValueError: Wenn User nicht existiert oder keine Stripe Customer ID
        """
        # 1. User laden
        user = await self.user_repo.get_by_id(request.user_id)
        if not user:
            raise ValueError(f"User {request.user_id} nicht gefunden")

        # 2. Stripe Customer ID prüfen
        if not user.stripe_customer_id:
            raise ValueError("User hat noch keine Stripe Subscription")

        # 3. Portal Session erstellen
        try:
            portal_url = await self.stripe_service.create_portal_session(
                stripe_customer_id=user.stripe_customer_id,
                return_url=request.return_url
            )
        except Exception as e:
            raise Exception(f"Fehler beim Erstellen der Portal Session: {str(e)}")

        # 4. Response zurückgeben
        return PortalSessionResponseDTO(
            portal_url=portal_url
        )
