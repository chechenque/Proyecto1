from pathlib import Path

from logitrack.services.offline_operation_service import (
    OfflineOperationService,
)


def test_queue_operation(tmp_path: Path) -> None:
    service = OfflineOperationService(
        tmp_path / "test.db",
    )

    operation = service.queue_operation(
        operation="postal_code_lookup",
        payload="01000",
    )

    assert operation.id is not None
    assert operation.status == "PENDING"


def test_get_pending_operations(tmp_path: Path) -> None:
    service = OfflineOperationService(
        tmp_path / "test.db",
    )

    service.queue_operation(
        operation="postal_code_lookup",
        payload="01000",
    )

    pending = service.get_pending_operations()

    assert len(pending) == 1
    assert pending[0].operation == "postal_code_lookup"
    assert pending[0].payload == "01000"

def test_mark_as_synced(tmp_path: Path) -> None:
    service = OfflineOperationService(
        tmp_path / "test.db",
    )

    operation = service.queue_operation(
        operation="postal_code_lookup",
        payload="01000",
    )

    assert operation.id is not None

    service.mark_as_synced(operation.id)

    pending = service.get_pending_operations()

    assert pending == []

def test_sync_operation_marks_operation_as_synced(
    tmp_path: Path,
) -> None:
    service = OfflineOperationService(
        tmp_path / "test.db",
    )

    operation = service.queue_operation(
        operation="postal_code_lookup",
        payload="01000",
    )

    assert service.sync_operation(operation) is True
    assert service.get_pending_operations() == []