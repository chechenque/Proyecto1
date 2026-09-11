from PyQt6.QtCore import QCoreApplication

from logitrack.services.shipment_service import ShipmentService
from logitrack.services.worker import ShipmentWorker




def test_worker_emits_finished() -> None:
    """El worker debe emitir finished al completar la operación."""

    app = QCoreApplication.instance()

    if app is None:
        app = QCoreApplication([])

    service = ShipmentService()

    class FastService:
        def simulate_long_operation(self) -> str:
            return service.simulate_long_operation(0.01)

    worker = ShipmentWorker(FastService())

    results: list[str] = []
    errors: list[str] = []

    worker.finished.connect(results.append)
    worker.error.connect(errors.append)

    worker.run()

    assert results == [
        "Operación completada correctamente."
    ]
    assert errors == []


def test_worker_emits_error() -> None:
    """El worker debe emitir error si el servicio falla."""

    app = QCoreApplication.instance()

    if app is None:
        app = QCoreApplication([])

    class FailingService:
        def simulate_long_operation(self) -> str:
            raise RuntimeError("Error de prueba")

    worker = ShipmentWorker(FailingService())

    results: list[str] = []
    errors: list[str] = []

    worker.finished.connect(results.append)
    worker.error.connect(errors.append)

    worker.run()

    assert results == []
    assert errors == ["Error de prueba"]