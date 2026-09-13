from pathlib import Path
import httpx
import pytest
from logitrack.services.address_api_client import AddressApiClient
from logitrack.services.shipment_service import ShipmentService


def test_service_creates_and_gets_shipment(
    tmp_path: Path,
) -> None:
    """Verifica que Service crea y recupera un envío."""

    service = ShipmentService(
        tmp_path / "test.db"
    )

    created = service.create_shipment(
        "María García",
        "Av. Universidad 100",
        "Nacional",
        "Pendiente",
    )

    shipments = service.get_shipments()

    assert created["recipient"] == "María García"
    assert len(shipments) == 1
    assert shipments[0]["recipient"] == "María García"


def test_service_searches_shipments(
    tmp_path: Path,
) -> None:
    """Verifica que Service delega correctamente la búsqueda."""

    service = ShipmentService(
        tmp_path / "test.db"
    )

    service.create_shipment(
        "Luis Hernández",
        "Av. Insurgentes 200",
        "Nacional",
        "En ruta",
    )

    service.create_shipment(
        "Laura Martínez",
        "Av. Reforma 300",
        "Internacional",
        "Pendiente",
    )

    results = service.search_shipments("Luis")

    assert len(results) == 1
    assert results[0]["recipient"] == "Luis Hernández"

    results = service.search_shipments("Reforma")

    assert len(results) == 1
    assert results[0]["recipient"] == "Laura Martínez"

def test_get_location_by_postal_code(tmp_path: Path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "places": [
                    {
                        "place name": "Álvaro Obregón",
                        "state": "Ciudad de México",
                    }
                ],
            },
        )

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)

    address_api_client = AddressApiClient(client)

    service = ShipmentService(
        tmp_path / "test.db",
        address_api_client,
    )

    result = service.get_location_by_postal_code("01000")

    assert result == {
        "city": "Álvaro Obregón",
        "state": "Ciudad de México",
    }

    address_api_client.close()

def test_queue_postal_code_lookup(tmp_path: Path) -> None:
    service = ShipmentService(
        tmp_path / "test.db",
    )

    service.queue_postal_code_lookup("01000")

    pending = (
        service.offline_operation_service
        .get_pending_operations()
    )

    assert len(pending) == 1
    assert pending[0].operation == "postal_code_lookup"
    assert pending[0].payload == "01000"
    assert pending[0].status == "PENDING"

def test_get_location_by_postal_code_queues_on_connection_error(
    tmp_path: Path,
) -> None:
    class FakeAddressApiClient:
        def get_location_by_postal_code(
            self,
            postal_code: str,
        ) -> dict[str, str]:
            raise ConnectionError(
                "No fue posible conectarse al servicio."
            )

    service = ShipmentService(
        tmp_path / "test.db",
        address_api_client=FakeAddressApiClient(),  # type: ignore[arg-type]
    )

    with pytest.raises(ConnectionError):
        service.get_location_by_postal_code("01000")

    pending = (
        service.offline_operation_service
        .get_pending_operations()
    )

    assert len(pending) == 1
    assert pending[0].operation == "postal_code_lookup"
    assert pending[0].payload == "01000"
    assert pending[0].status == "PENDING"