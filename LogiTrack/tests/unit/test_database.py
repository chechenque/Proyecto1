from pathlib import Path

from logitrack.models.database import Database


def test_initialize_creates_offline_operations_table(
    tmp_path: Path,
) -> None:
    database = Database(tmp_path / "test.db")

    database.initialize()

    with database.connect() as connection:
        row = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'offline_operations'
            """
        ).fetchone()

    assert row is not None
    assert row["name"] == "offline_operations"