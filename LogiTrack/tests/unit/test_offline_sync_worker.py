from logitrack.services.offline_sync_worker import (
    OfflineSyncWorker,
)


def test_offline_sync_worker_emits_finished() -> None:
    class FakeService:
        def sync_pending_postal_code_operations(self) -> int:
            return 3

    worker = OfflineSyncWorker(
        FakeService(),  # type: ignore[arg-type]
    )

    results: list[int] = []

    worker.finished.connect(
        lambda count: results.append(count)
    )

    worker.run()

    assert results == [3]