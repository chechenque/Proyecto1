from logitrack.controllers.offline_operation_controller import (
    OfflineOperationController,
)


def test_queue_operation() -> None:
    class FakeService:
        def queue_operation(
            self,
            operation: str,
            payload: str,
            status: str,
        ) -> dict[str, str]:
            assert operation == "postal_code_lookup"
            assert payload == "01000"
            assert status == "PENDING"

            return {
                "operation": operation,
                "payload": payload,
                "status": status,
            }

    controller = OfflineOperationController(FakeService())  # type: ignore[arg-type]

    result = controller.queue_operation(
        "postal_code_lookup",
        "01000",
    )

    assert result["status"] == "PENDING"


def test_get_pending_operations() -> None:
    class FakeService:
        def get_pending_operations(self) -> list[dict[str, str]]:
            return [
                {
                    "operation": "postal_code_lookup",
                    "payload": "01000",
                    "status": "PENDING",
                }
            ]

    controller = OfflineOperationController(FakeService())  # type: ignore[arg-type]

    result = controller.get_pending_operations()

    assert len(result) == 1
    assert result[0]["payload"] == "01000"


def test_mark_as_synced() -> None:
    class FakeService:
        def mark_as_synced(self, operation_id: int) -> None:
            assert operation_id == 1

    controller = OfflineOperationController(FakeService())  # type: ignore[arg-type]

    controller.mark_as_synced(1)