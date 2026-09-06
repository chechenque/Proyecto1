class ShipmentController:
    """Controlador de las operaciones relacionadas con envíos."""

    def __init__(self) -> None:
        self.shipments: list[dict[str, str]] = []

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

        shipment = {
            "recipient": recipient,
            "address": address,
            "type": shipment_type,
            "status": status,
        }

        self.shipments.append(shipment)

        return True, "Envío registrado correctamente."

    def search_shipments(
        self,
        search_text: str,
    ) -> list[dict[str, str]]:
        """Busca envíos por destinatario o dirección."""

        search_text = search_text.strip().lower()

        if not search_text:
            return self.shipments.copy()

        return [
            shipment
            for shipment in self.shipments
            if search_text in shipment["recipient"].lower()
            or search_text in shipment["address"].lower()
        ]

