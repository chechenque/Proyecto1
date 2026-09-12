from pathlib import Path

from logitrack.controllers.shipment_controller import (
    ShipmentController,
)
from logitrack.services.shipment_service import ShipmentService


def create_controller(
    tmp_path: Path,
) -> ShipmentController:
    """Crea un Controller utilizando una base temporal."""

    service = ShipmentService(
        tmp_path / "test.db"
    )

    return ShipmentController(service)


def test_create_shipment_requires_recipient(
    tmp_path: Path,
) -> None:
    """El destinatario debe ser obligatorio."""

    controller = create_controller(tmp_path)

    success, message = controller.create_shipment(
        "",
        "Av. Reforma 123",
        "Nacional",
        "Pendiente",
    )

    assert success is False
    assert message == "El destinatario es obligatorio."


def test_create_shipment_requires_address(
    tmp_path: Path,
) -> None:
    """La dirección debe ser obligatoria."""

    controller = create_controller(tmp_path)

    success, message = controller.create_shipment(
        "Ana López",
        "",
        "Nacional",
        "Pendiente",
    )

    assert success is False
    assert message == "La dirección es obligatoria."


def test_create_shipment_success(
    tmp_path: Path,
) -> None:
    """Un envío válido debe registrarse correctamente."""

    controller = create_controller(tmp_path)

    success, message = controller.create_shipment(
        "Ana López",
        "Av. Reforma 123",
        "Nacional",
        "Pendiente",
    )

    assert success is True
    assert message == "Envío registrado correctamente."

    shipments = controller.get_shipments()

    assert len(shipments) == 1
    assert shipments[0]["recipient"] == "Ana López"

def test_get_location_by_postal_code() -> None:
    class FakeService:
        def get_location_by_postal_code(
            self,
            postal_code: str,
        ) -> dict[str, str]:
            assert postal_code == "01000"
            return {
                "city": "Álvaro Obregón",
                "state": "Ciudad de México",
            }

    controller = ShipmentController(FakeService())

    result = controller.get_location_by_postal_code("01000")

    assert result == {
        "city": "Álvaro Obregón",
        "state": "Ciudad de México",
    }