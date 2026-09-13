from pathlib import Path

from logitrack.models.database import Database
from logitrack.models.offline_operation_repository import (
    OfflineOperationRepository,
)


def create_repository(tmp_path: Path) -> OfflineOperationRepository:
    database = Database(tmp_path / "test.db")
    database.initialize()

    return OfflineOperationRepository(database)


def test_create_offline_operation(tmp_path: Path) -> None:
    repository = create_repository(tmp_path)

    operation = repository.create(
        operation="postal_code_lookup",
        payload="01000",
        status="PENDING",
    )

    assert operation.id is not None
    assert operation.operation == "postal_code_lookup"
    assert operation.payload == "01000"
    assert operation.status == "PENDING"


def test_get_pending_returns_pending_operations(
    tmp_path: Path,
) -> None:
    repository = create_repository(tmp_path)

    repository.create(
        operation="postal_code_lookup",
        payload="01000",
        status="PENDING",
    )

    repository.create(
        operation="postal_code_lookup",
        payload="99999",
        status="SYNCED",
    )

    pending = repository.get_pending()

    assert len(pending) == 1
    assert pending[0].payload == "01000"
    assert pending[0].status == "PENDING"

def test_mark_as_synced(tmp_path: Path) -> None:
    repository = create_repository(tmp_path)

    operation = repository.create(
        operation="postal_code_lookup",
        payload="01000",
        status="PENDING",
    )

    assert operation.id is not None

    repository.mark_as_synced(operation.id)

    pending = repository.get_pending()

    assert pending == []