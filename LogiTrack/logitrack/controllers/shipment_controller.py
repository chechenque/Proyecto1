from logitrack.services.shipment_service import ShipmentService
from pydantic import ValidationError


class ShipmentController:
    """Controlador de las operaciones relacionadas con envíos."""

    def __init__(
            self,
            service: ShipmentService | None = None,
    ) -> None:
        self.service = (
            service
            if service is not None
            else ShipmentService()
        )

    def create_shipment(
            self,
            recipient: str,
            address: str,
            shipment_type: str,
            status: str,
    ) -> tuple[bool, str]:
        """Valida y crea un envío."""

        try:
            self.service.create_shipment(
                recipient,
                address,
                shipment_type,
                status,
            )
        except ValidationError as exc:
            first_error = exc.errors()[0]
            field = first_error["loc"][0]
            message = str(first_error["msg"])

            if field == "recipient":
                return False, "El destinatario es obligatorio."

            if field == "address":
                return False, "La dirección es obligatoria."

            return False, message

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

    def get_location_by_postal_code(
        self,
        postal_code: str,
    ) -> dict[str, str]:
        """Consulta la ubicación de un código postal."""

        return self.service.get_location_by_postal_code(
            postal_code
        )