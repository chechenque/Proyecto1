import sqlite3

from logitrack.models.database import Database
from logitrack.models.shipment import Shipment


class ShipmentRepository:
    """Persistencia de envíos mediante SQLite."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def _row_to_shipment(
            self,
            row: sqlite3.Row,
    ) -> Shipment:
        """Convierte una fila SQLite en un modelo Shipment."""

        return Shipment(
            id=row["id"],
            recipient=row["recipient"],
            address=row["address"],
            shipment_type=row["shipment_type"],
            status=row["status"],
        )

    def create(
            self,
            recipient: str,
            address: str,
            shipment_type: str,
            status: str,
    ) -> dict[str, str]:
        """Valida y guarda un envío en la base de datos."""

        shipment = Shipment(
            recipient=recipient,
            address=address,
            shipment_type=shipment_type,
            status=status,
        )

        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO shipments (recipient,
                                       address,
                                       shipment_type,
                                       status)
                VALUES (?, ?, ?, ?)
                """,
                (
                    shipment.recipient,
                    shipment.address,
                    shipment.shipment_type,
                    shipment.status,
                ),
            )
            connection.commit()
            shipment_id = cursor.lastrowid

        return {
            "id": str(shipment_id),
            "recipient": shipment.recipient,
            "address": shipment.address,
            "type": shipment.shipment_type,
            "status": shipment.status,
        }

    def get_all(self) -> list[dict[str, str]]:
        """Obtiene todos los envíos."""

        with self.database.connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    recipient,
                    address,
                    shipment_type,
                    status
                FROM shipments
                ORDER BY id
                """
            ).fetchall()

        return [
            {
                "id": str(shipment.id),
                "recipient": shipment.recipient,
                "address": shipment.address,
                "type": shipment.shipment_type,
                "status": shipment.status,
            }
            for row in rows
            for shipment in [self._row_to_shipment(row)]
        ]

    def search(
        self,
        search_text: str,
    ) -> list[dict[str, str]]:
        """Busca envíos por destinatario o dirección."""

        search_text = search_text.strip()

        if not search_text:
            return self.get_all()

        pattern = f"%{search_text}%"

        with self.database.connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    recipient,
                    address,
                    shipment_type,
                    status
                FROM shipments
                WHERE recipient LIKE ?
                   OR address LIKE ?
                ORDER BY id
                """,
                (pattern, pattern),
            ).fetchall()

        return [
            {
                "id": str(shipment.id),
                "recipient": shipment.recipient,
                "address": shipment.address,
                "type": shipment.shipment_type,
                "status": shipment.status,
            }
            for row in rows
            for shipment in [self._row_to_shipment(row)]
        ]