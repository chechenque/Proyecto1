from logitrack.config import DATABASE_PATH
from logitrack.models.database import Database
from logitrack.models.shipment_repository import ShipmentRepository
from pathlib import Path
from logitrack.services.address_api_client import AddressApiClient
from PyQt6.QtCore import QObject, pyqtSignal
from logitrack.services.offline_operation_service import (
    OfflineOperationService,
)


class ShipmentService:
    """Servicios relacionados con la gestión de envíos."""

    def __init__(
            self,
            database_path: str | Path | None = None,
            address_api_client: AddressApiClient | None = None,
            offline_operation_service: OfflineOperationService | None = None,
    ) -> None:
        if database_path is None:
            database_path = DATABASE_PATH

        database = Database(database_path)
        database.initialize()

        self.repository = ShipmentRepository(database)

        self.address_api_client = (
            address_api_client
            if address_api_client is not None
            else AddressApiClient()
        )

        self.offline_operation_service = (
            offline_operation_service
            if offline_operation_service is not None
            else OfflineOperationService(database_path)
        )

    def create_shipment(
        self,
        recipient: str,
        address: str,
        shipment_type: str,
        status: str,
    ) -> dict[str, str]:
        """Crea y persiste un envío."""

        return self.repository.create(
            recipient,
            address,
            shipment_type,
            status,
        )

    def search_shipments(
        self,
        search_text: str,
    ) -> list[dict[str, str]]:
        """Busca envíos almacenados."""

        return self.repository.search(search_text)

    def get_shipments(self) -> list[dict[str, str]]:
        """Obtiene todos los envíos almacenados."""

        return self.repository.get_all()

    def simulate_long_operation(
            self,
            delay: float = 5.0,
    ) -> str:
        """Simula una operación que tarda algunos segundos."""
        import time

        time.sleep(delay)

        return "Operación completada correctamente."

    def get_location_by_postal_code(
            self,
            postal_code: str,
    ) -> dict[str, str]:
        """Consulta la ubicación asociada a un código postal."""

        try:
            return self.address_api_client.get_location_by_postal_code(
                postal_code
            )
        except ConnectionError:
            self.queue_postal_code_lookup(postal_code)
            raise

    def queue_postal_code_lookup(
            self,
            postal_code: str,
    ) -> None:
        """Agrega una consulta de código postal a la cola offline."""

        self.offline_operation_service.queue_operation(
            operation="postal_code_lookup",
            payload=postal_code,
        )