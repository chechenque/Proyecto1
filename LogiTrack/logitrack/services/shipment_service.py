import time


class ShipmentService:
    """Servicios relacionados con la gestión de envíos."""

    def simulate_long_operation(self) -> str:
        """Simula una operación que tarda algunos segundos."""
        time.sleep(5)
        return "Operación completada correctamente."