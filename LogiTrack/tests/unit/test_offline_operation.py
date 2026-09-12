import pytest
from pydantic import ValidationError

from logitrack.models.offline_operation import OfflineOperation


def test_offline_operation_strips_whitespace() -> None:
    operation = OfflineOperation(
        operation="  postal_code_lookup  ",
        payload="  01000  ",
        status="  PENDING  ",
    )

    assert operation.operation == "postal_code_lookup"
    assert operation.payload == "01000"
    assert operation.status == "PENDING"


def test_offline_operation_rejects_empty_operation() -> None:
    with pytest.raises(ValidationError):
        OfflineOperation(
            operation="",
            payload="01000",
            status="PENDING",
        )


def test_offline_operation_rejects_empty_payload() -> None:
    with pytest.raises(ValidationError):
        OfflineOperation(
            operation="postal_code_lookup",
            payload="",
            status="PENDING",
        )


def test_offline_operation_rejects_empty_status() -> None:
    with pytest.raises(ValidationError):
        OfflineOperation(
            operation="postal_code_lookup",
            payload="01000",
            status="",
        )