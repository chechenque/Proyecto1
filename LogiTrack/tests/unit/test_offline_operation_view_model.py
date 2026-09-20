from logitrack.controllers.offline_operation_view_model import (
    OfflineOperationViewModel,
)


def test_queue_operation_emits_signal() -> None:
    class FakeController:
        def queue_operation(
            self,
            operation: str,
            payload: str,
            status: str,
        ) -> None:
            assert operation == "postal_code_lookup"
            assert payload == "01000"
            assert status == "PENDING"

    controller = FakeController()

    view_model = OfflineOperationViewModel(controller)  # type: ignore[arg-type]

    emitted = []
    view_model.operations_changed.connect(
        lambda: emitted.append(True)
    )

    view_model.queue_operation(
        "postal_code_lookup",
        "01000",
    )

    assert emitted == [True]


def test_get_pending_operations() -> None:
    class FakeController:
        def get_pending_operations(self) -> list[dict[str, str]]:
            return [
                {
                    "operation": "postal_code_lookup",
                    "payload": "01000",
                    "status": "PENDING",
                }
            ]

    view_model = OfflineOperationViewModel(  # type: ignore[arg-type]
        FakeController()
    )

    result = view_model.get_pending_operations()

    assert len(result) == 1
    assert result[0]["payload"] == "01000"


def test_count_pending() -> None:
    class FakeController:
        def get_pending_operations(self) -> list[dict[str, str]]:
            return [
                {
                    "operation": "postal_code_lookup",
                    "payload": "01000",
                    "status": "PENDING",
                },
                {
                    "operation": "postal_code_lookup",
                    "payload": "99999",
                    "status": "PENDING",
                },
            ]

    view_model = OfflineOperationViewModel(  # type: ignore[arg-type]
        FakeController()
    )

    assert view_model.count_pending() == 2


def test_mark_as_synced_emits_signal() -> None:
    class FakeController:
        def mark_as_synced(self, operation_id: int) -> None:
            assert operation_id == 1

    view_model = OfflineOperationViewModel(  # type: ignore[arg-type]
        FakeController()
    )

    emitted = []
    view_model.operations_changed.connect(
        lambda: emitted.append(True)
    )

    view_model.mark_as_synced(1)

    assert emitted == [True]