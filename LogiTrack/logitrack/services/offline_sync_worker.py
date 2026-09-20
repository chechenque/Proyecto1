from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from logitrack.services.shipment_service import ShipmentService


class OfflineSyncWorker(QObject):
    """Sincroniza operaciones offline fuera del hilo de la interfaz."""

    finished = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(
        self,
        service: ShipmentService,
    ) -> None:
        super().__init__()
        self.service = service

    @pyqtSlot()
    def run(self) -> None:
        """Ejecuta la sincronización de operaciones pendientes."""

        try:
            synchronized = (
                self.service
                .sync_pending_postal_code_operations()
            )

            self.finished.emit(synchronized)

        except Exception as exc:
            self.error.emit(str(exc))