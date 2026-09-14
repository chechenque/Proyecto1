from pathlib import Path

from logitrack.config import DATABASE_PATH
from logitrack.models.database import Database
from logitrack.models.offline_operation import OfflineOperation
from logitrack.models.offline_operation_repository import (
    OfflineOperationRepository,
)


class OfflineOperationService:
    """Gestiona las operaciones pendientes de sincronización."""

    def __init__(
        self,
        database_path: str | Path | None = None,
    ) -> None:
        if database_path is None:
            database_path = DATABASE_PATH

        database = Database(database_path)
        database.initialize()

        self.repository = OfflineOperationRepository(database)

    def queue_operation(
        self,
        operation: str,
        payload: str,
        status: str = "PENDING",
    ) -> OfflineOperation:
        """Agrega una operación a la cola offline."""

        return self.repository.create(
            operation,
            payload,
            status,
        )

    def get_pending_operations(self) -> list[OfflineOperation]:
        """Obtiene las operaciones pendientes."""

        return self.repository.get_pending()

    def mark_as_synced(self, operation_id: int) -> None:
        """Marca una operación como sincronizada."""

        self.repository.mark_as_synced(operation_id)

    def sync_operation(
            self,
            operation: OfflineOperation,
    ) -> bool:
        """Marca una operación como sincronizada."""

        if operation.id is None:
            return False

        self.mark_as_synced(operation.id)
        return True