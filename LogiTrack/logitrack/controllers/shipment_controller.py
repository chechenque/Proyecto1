from logitrack.services.shipment_service import ShipmentService


class ShipmentController:
    """Controlador de las operaciones relacionadas con envíos."""

    def __init__(self) -> None:
        self.service = ShipmentService()

    def create_shipment(
        self,
        recipient: str,
        address: str,
        shipment_type: str,
        status: str,
    ) -> tuple[bool, str]:
        """Valida y registra un nuevo envío."""

        recipient = recipient.strip()
        address = address.strip()

        if not recipient:
            return False, "El destinatario es obligatorio."

        if not address:
            return False, "La dirección es obligatoria."

        self.service.create_shipment(
            recipient,
            address,
            shipment_type,
            status,
        )

        return True, "Envío registrado correctamente."

    def search_shipments(
        self,
        search_text: str,
    ) -> list[dict[str, str]]:
        """Busca envíos por destinatario o dirección."""

        return self.service.search_shipments(search_text)

    def get_shipments(self) -> list[dict[str, str]]:
        """Obtiene todos los envíos registrados."""
        return self.service.search_shipments("")

    def get_service(self) -> ShipmentService:
        """Devuelve el servicio utilizado por el controlador."""
        return self.service