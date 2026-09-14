from pathlib import Path

from logitrack.models.offline_operation import OfflineOperation
from logitrack.services.offline_operation_service import (
    OfflineOperationService,
)


class OfflineOperationController:
    """Controlador de las operaciones offline."""

    def __init__(
        self,
        service: OfflineOperationService | None = None,
    ) -> None:
        self.service = (
            service
            if service is not None
            else OfflineOperationService()
        )

    def queue_operation(
        self,
        operation: str,
        payload: str,
        status: str = "PENDING",
    ) -> OfflineOperation:
        """Agrega una operación a la cola offline."""

        return self.service.queue_operation(
            operation,
            payload,
            status,
        )

    def get_pending_operations(self) -> list[OfflineOperation]:
        """Obtiene las operaciones pendientes."""

        return self.service.get_pending_operations()

    def mark_as_synced(self, operation_id: int) -> None:
        """Marca una operación como sincronizada."""

        self.service.mark_as_synced(operation_id)

