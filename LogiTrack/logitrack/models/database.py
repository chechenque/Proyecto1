import sqlite3
from pathlib import Path


class Database:
    """Gestiona la conexión y estructura de la base de datos SQLite."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def connect(self) -> sqlite3.Connection:
        """Crea una conexión con la base de datos."""

        connection = sqlite3.connect(
            self.database_path
        )
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        """Crea las tablas necesarias si todavía no existen."""

        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS shipments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipient TEXT NOT NULL,
                    address TEXT NOT NULL,
                    shipment_type TEXT NOT NULL,
                    status TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS offline_operations
                (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation TEXT NOT NULL,
                    payload   TEXT NOT NULL,
                    status    TEXT NOT NULL
                )
                """
            )

            connection.commit()