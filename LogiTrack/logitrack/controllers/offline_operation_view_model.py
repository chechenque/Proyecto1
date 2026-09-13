from PyQt6.QtCore import QObject, pyqtSignal

from logitrack.controllers.offline_operation_controller import (
    OfflineOperationController,
)


class OfflineOperationViewModel(QObject):
    """ViewModel para gestionar operaciones offline."""

    operations_changed = pyqtSignal()

    def __init__(
        self,
        controller: OfflineOperationController,
    ) -> None:
        super().__init__()
        self.controller = controller

    def queue_operation(
        self,
        operation: str,
        payload: str,
        status: str = "PENDING",
    ) -> None:
        """Agrega una operación a la cola."""

        self.controller.queue_operation(
            operation,
            payload,
            status,
        )

        self.operations_changed.emit()

    def get_pending_operations(self) -> list:
        """Obtiene las operaciones pendientes."""

        return self.controller.get_pending_operations()

    def count_pending(self) -> int:
        """Obtiene el número de operaciones pendientes."""

        return len(self.get_pending_operations())

    def mark_as_synced(self, operation_id: int) -> None:
        """Marca una operación como sincronizada."""

        self.controller.mark_as_synced(operation_id)
        self.operations_changed.emit()