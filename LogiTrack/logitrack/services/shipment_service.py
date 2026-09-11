from logitrack.config import DATABASE_PATH
from logitrack.models.database import Database
from logitrack.models.shipment_repository import ShipmentRepository
from pathlib import Path


class ShipmentService:
    """Servicios relacionados con la gestión de envíos."""

    def __init__(
            self,
            database_path: str | Path | None = None,
    ) -> None:
        if database_path is None:
            database_path = DATABASE_PATH

        database = Database(database_path)
        database.initialize()

        self.repository = ShipmentRepository(database)

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