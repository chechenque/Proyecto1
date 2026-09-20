import pytest
from pydantic import ValidationError

from logitrack.models.shipment import Shipment


def test_shipment_strips_whitespace() -> None:
    """El modelo debe eliminar espacios innecesarios."""

    shipment = Shipment(
        recipient=" Ana López ",
        address=" Av. Reforma 123 ",
        shipment_type=" Nacional ",
        status=" Pendiente ",
    )

    assert shipment.recipient == "Ana López"
    assert shipment.address == "Av. Reforma 123"
    assert shipment.shipment_type == "Nacional"
    assert shipment.status == "Pendiente"


def test_shipment_requires_recipient() -> None:
    """El destinatario debe ser obligatorio."""

    with pytest.raises(ValidationError):
        Shipment(
            recipient="",
            address="Av. Reforma 123",
            shipment_type="Nacional",
            status="Pendiente",
        )


def test_shipment_requires_address() -> None:
    """La dirección debe ser obligatoria."""

    with pytest.raises(ValidationError):
        Shipment(
            recipient="Ana López",
            address="",
            shipment_type="Nacional",
            status="Pendiente",
        )

def test_shipment_rejects_long_recipient() -> None:
    """El destinatario no debe superar 100 caracteres."""

    with pytest.raises(ValidationError):
        Shipment(
            recipient="A" * 101,
            address="Av. Reforma 123",
            shipment_type="Nacional",
            status="Pendiente",
        )


def test_shipment_rejects_long_address() -> None:
    """La dirección no debe superar 250 caracteres."""

    with pytest.raises(ValidationError):
        Shipment(
            recipient="Ana López",
            address="A" * 251,
            shipment_type="Nacional",
            status="Pendiente",
        )