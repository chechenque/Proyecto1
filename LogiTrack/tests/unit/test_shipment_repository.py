from pathlib import Path

from logitrack.models.database import Database
from logitrack.models.shipment_repository import ShipmentRepository


def test_create_and_get_shipment(tmp_path: Path) -> None:
    """Verifica que un envío se guarda y puede recuperarse."""

    database = Database(
        tmp_path / "test.db"
    )
    database.initialize()

    repository = ShipmentRepository(database)

    created = repository.create(
        "Ana López",
        "Av. Reforma 123",
        "Nacional",
        "Pendiente",
    )

    shipments = repository.get_all()

    assert len(shipments) == 1
    assert created["recipient"] == "Ana López"
    assert shipments[0]["recipient"] == "Ana López"
    assert shipments[0]["address"] == "Av. Reforma 123"
    assert shipments[0]["type"] == "Nacional"
    assert shipments[0]["status"] == "Pendiente"

def test_search_shipments(tmp_path: Path) -> None:
    """Verifica la búsqueda por destinatario y dirección."""

    database = Database(
        tmp_path / "test.db"
    )
    database.initialize()

    repository = ShipmentRepository(database)

    repository.create(
        "Ana López",
        "Av. Reforma 123",
        "Nacional",
        "Pendiente",
    )

    repository.create(
        "Carlos Pérez",
        "Insurgentes Sur 456",
        "Internacional",
        "En ruta",
    )

    recipient_results = repository.search("Ana")

    assert len(recipient_results) == 1
    assert recipient_results[0]["recipient"] == "Ana López"

    address_results = repository.search("Insurgentes")

    assert len(address_results) == 1
    assert address_results[0]["recipient"] == "Carlos Pérez"

def test_row_to_shipment(
    tmp_path: Path,
) -> None:
    """Una fila SQLite debe convertirse en un Shipment válido."""

    database = Database(tmp_path / "test.db")
    database.initialize()

    repository = ShipmentRepository(database)

    with database.connect() as connection:
        connection.execute(
            """
            INSERT INTO shipments (
                recipient,
                address,
                shipment_type,
                status
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                "Ana López",
                "Av. Reforma 123",
                "Nacional",
                "Pendiente",
            ),
        )
        connection.commit()

        row = connection.execute(
            "SELECT * FROM shipments"
        ).fetchone()

    shipment = repository._row_to_shipment(row)

    assert shipment.id is not None
    assert shipment.recipient == "Ana López"
    assert shipment.address == "Av. Reforma 123"
    assert shipment.shipment_type == "Nacional"
    assert shipment.status == "Pendiente"