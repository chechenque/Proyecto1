from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from logitrack.services.shipment_service import ShipmentService


class ShipmentWorker(QObject):
    """Ejecuta operaciones de envíos fuera del hilo de la interfaz."""

    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, service: ShipmentService) -> None:
        super().__init__()
        self.service = service

    @pyqtSlot()
    def run(self) -> None:
        """Ejecuta la operación de larga duración."""
        try:
            result = self.service.simulate_long_operation()
            self.finished.emit(result)
        except Exception as exc:
            self.error.emit(str(exc))