from pathlib import Path

from logitrack.controllers.shipment_controller import (
    ShipmentController,
)
from logitrack.controllers.shipment_view_model import (
    ShipmentViewModel,
)
from logitrack.models.shipment_table_model import (
    ShipmentTableModel,
)
from logitrack.services.shipment_service import ShipmentService


def create_view_model(
    tmp_path: Path,
) -> ShipmentViewModel:
    """Crea un ViewModel con una base temporal."""

    service = ShipmentService(
        tmp_path / "test.db"
    )

    controller = ShipmentController(service)

    model = ShipmentTableModel(
        controller.get_shipments()
    )

    return ShipmentViewModel(
        controller,
        model,
    )


def test_view_model_create_shipment(
    tmp_path: Path,
) -> None:
    """Verifica que ViewModel crea y actualiza un envío."""

    view_model = create_view_model(tmp_path)

    success, message = view_model.create_shipment(
        "Ana López",
        "Av. Reforma 123",
        "Nacional",
        "Pendiente",
    )

    assert success is True
    assert message == "Envío registrado correctamente."
    assert view_model.count() == 1
    assert len(view_model.shipment_model.shipments) == 1


def test_view_model_search(
    tmp_path: Path,
) -> None:
    """Verifica que ViewModel busca y actualiza la tabla."""

    view_model = create_view_model(tmp_path)

    view_model.create_shipment(
        "Ana López",
        "Av. Reforma 123",
        "Nacional",
        "Pendiente",
    )

    view_model.create_shipment(
        "Carlos Pérez",
        "Insurgentes Sur 456",
        "Internacional",
        "En ruta",
    )

    result_count = view_model.search("Ana")

    assert result_count == 1
    assert len(view_model.shipment_model.shipments) == 1
    assert (
        view_model.shipment_model.shipments[0]["recipient"]
        == "Ana López"
    )


def test_view_model_refresh(
    tmp_path: Path,
) -> None:
    """Verifica que refresh recupera todos los envíos."""

    view_model = create_view_model(tmp_path)

    view_model.create_shipment(
        "Ana López",
        "Av. Reforma 123",
        "Nacional",
        "Pendiente",
    )

    view_model.create_shipment(
        "Carlos Pérez",
        "Insurgentes Sur 456",
        "Internacional",
        "En ruta",
    )

    view_model.search("Ana")

    assert len(view_model.shipment_model.shipments) == 1

    view_model.refresh()

    assert len(view_model.shipment_model.shipments) == 2
    assert view_model.count() == 2