from logitrack.models.database import Database
from logitrack.models.offline_operation import OfflineOperation


class OfflineOperationRepository:
    """Persistencia de operaciones pendientes en SQLite."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def create(
        self,
        operation: str,
        payload: str,
        status: str,
    ) -> OfflineOperation:
        """Guarda una operación offline."""

        offline_operation = OfflineOperation(
            operation=operation,
            payload=payload,
            status=status,
        )

        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO offline_operations (
                    operation,
                    payload,
                    status
                )
                VALUES (?, ?, ?)
                """,
                (
                    offline_operation.operation,
                    offline_operation.payload,
                    offline_operation.status,
                ),
            )

            offline_operation.id = cursor.lastrowid

        return offline_operation

    def get_pending(self) -> list[OfflineOperation]:
        """Obtiene las operaciones pendientes."""

        with self.database.connect() as connection:
            rows = connection.execute(
                """
                SELECT id, operation, payload, status
                FROM offline_operations
                WHERE status = ?
                ORDER BY id
                """,
                ("PENDING",),
            ).fetchall()

        return [
            OfflineOperation(
                id=row["id"],
                operation=row["operation"],
                payload=row["payload"],
                status=row["status"],
            )
            for row in rows
        ]

    def mark_as_synced(self, operation_id: int) -> None:
        """Marca una operación como sincronizada."""

        with self.database.connect() as connection:
            connection.execute(
                """
                UPDATE offline_operations
                SET status = ?
                WHERE id = ?
                """,
                ("SYNCED", operation_id),
            )