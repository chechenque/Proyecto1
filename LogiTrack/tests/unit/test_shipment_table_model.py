from PyQt6.QtCore import Qt

from logitrack.models.shipment_table_model import (
    ShipmentTableModel,
)


def create_model() -> ShipmentTableModel:
    """Crea un modelo con datos de prueba."""

    shipments = [
        {
            "id": "1",
            "recipient": "Carlos Pérez",
            "address": "Insurgentes Sur 456",
            "type": "Internacional",
            "status": "En ruta",
        },
        {
            "id": "2",
            "recipient": "Ana López",
            "address": "Av. Reforma 123",
            "type": "Nacional",
            "status": "Pendiente",
        },
        {
            "id": "3",
            "recipient": "Luis Hernández",
            "address": "Av. Universidad 100",
            "type": "Nacional",
            "status": "Entregado",
        },
    ]

    return ShipmentTableModel(shipments)


def test_model_row_and_column_count() -> None:
    """Verifica la cantidad de filas y columnas."""

    model = create_model()

    assert model.rowCount() == 3
    assert model.columnCount() == 4


def test_model_display_data() -> None:
    """Verifica los valores mostrados en la tabla."""

    model = create_model()

    index = model.index(0, 0)

    assert model.data(
        index,
        Qt.ItemDataRole.DisplayRole,
    ) == "Carlos Pérez"

    index = model.index(1, 3)

    assert model.data(
        index,
        Qt.ItemDataRole.DisplayRole,
    ) == "Pendiente"


def test_model_headers() -> None:
    """Verifica los encabezados de la tabla."""

    model = create_model()

    assert model.headerData(
        0,
        Qt.Orientation.Horizontal,
    ) == "Destinatario"

    assert model.headerData(
        3,
        Qt.Orientation.Horizontal,
    ) == "Estado"


def test_model_sort_ascending() -> None:
    """Verifica el ordenamiento ascendente."""

    model = create_model()

    model.sort(
        0,
        Qt.SortOrder.AscendingOrder,
    )

    assert model.shipments[0]["recipient"] == "Ana López"
    assert model.shipments[1]["recipient"] == "Carlos Pérez"
    assert model.shipments[2]["recipient"] == "Luis Hernández"


def test_model_sort_descending() -> None:
    """Verifica el ordenamiento descendente."""

    model = create_model()

    model.sort(
        0,
        Qt.SortOrder.DescendingOrder,
    )

    assert model.shipments[0]["recipient"] == "Luis Hernández"
    assert model.shipments[1]["recipient"] == "Carlos Pérez"
    assert model.shipments[2]["recipient"] == "Ana López"


def test_model_foreground_for_statuses() -> None:
    """Verifica el color de texto según el estado."""

    model = create_model()

    expected_colors = {
        "Entregado": "#188038",
        "En ruta": "#1967d2",
        "Retrasado": "#d93025",
        "Pendiente": "#b06000",
    }

    for row, status in enumerate(expected_colors):
        model.shipments.append(
            {
                "id": str(row + 4),
                "recipient": "Prueba",
                "address": "Dirección",
                "type": "Nacional",
                "status": status,
            }
        )

    for row, expected in enumerate(expected_colors, start=3):
        index = model.index(row, 3)

        color = model.data(
            index,
            Qt.ItemDataRole.ForegroundRole,
        )

        assert color.name() == expected_colors[expected]


def test_model_background_for_statuses() -> None:
    """Verifica el fondo de la columna Estado."""

    model = create_model()

    expected_colors = {
        "Entregado": "#e6f4ea",
        "En ruta": "#e8f0fe",
        "Retrasado": "#fce8e6",
        "Pendiente": "#fef7e0",
    }

    for status, expected_color in expected_colors.items():
        model.shipments.append(
            {
                "id": "10",
                "recipient": "Prueba",
                "address": "Dirección",
                "type": "Nacional",
                "status": status,
            }
        )

        index = model.index(
            model.rowCount() - 1,
            3,
        )

        color = model.data(
            index,
            Qt.ItemDataRole.BackgroundRole,
        )

        assert color.name() == expected_color


def test_model_background_only_applies_to_status_column() -> None:
    """El fondo especial solo aplica a la columna Estado."""

    model = create_model()

    index = model.index(0, 0)

    assert model.data(
        index,
        Qt.ItemDataRole.BackgroundRole,
    ) is None


def test_model_invalid_index_returns_none() -> None:
    """Un índice inválido no debe devolver datos."""

    model = create_model()

    index = model.index(-1, -1)

    assert model.data(index) is None


def test_model_vertical_header() -> None:
    """Verifica los encabezados numéricos de las filas."""

    model = create_model()

    assert model.headerData(
        0,
        Qt.Orientation.Vertical,
    ) == "1"

    assert model.headerData(
        2,
        Qt.Orientation.Vertical,
    ) == "3"


def test_model_update_shipments() -> None:
    """Verifica la actualización de los datos del modelo."""

    model = create_model()

    new_shipments = [
        {
            "id": "20",
            "recipient": "Nuevo Usuario",
            "address": "Nueva dirección",
            "type": "Nacional",
            "status": "Pendiente",
        }
    ]

    model.update_shipments(new_shipments)

    assert model.rowCount() == 1
    assert model.shipments[0]["recipient"] == "Nuevo Usuario"