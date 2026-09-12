from PyQt6.QtCore import QObject, pyqtSignal

from logitrack.models.shipment_table_model import ShipmentTableModel


class ShipmentViewModel(QObject):
    """ViewModel que conecta los datos con la interfaz."""

    shipments_changed = pyqtSignal()

    def __init__(
        self,
        controller,
        shipment_model: ShipmentTableModel,
    ) -> None:
        super().__init__()

        self.controller = controller
        self.shipment_model = shipment_model

    def refresh(self) -> None:
        """Actualiza los envíos mostrados en la tabla."""

        shipments = self.controller.get_shipments()

        self.shipment_model.update_shipments(
            shipments
        )

        self.shipments_changed.emit()

    def search(self, search_text: str) -> int:
        """Busca envíos y actualiza la tabla."""

        shipments = self.controller.search_shipments(
            search_text
        )

        self.shipment_model.update_shipments(
            shipments
        )

        self.shipments_changed.emit()

        return len(shipments)

    def count(self) -> int:
        """Devuelve la cantidad de envíos registrados."""

        return len(
            self.controller.get_shipments()
        )

    def create_shipment(
            self,
            recipient: str,
            address: str,
            shipment_type: str,
            status: str,
    ) -> tuple[bool, str]:
        """Solicita al controlador la creación de un envío."""

        success, message = self.controller.create_shipment(
            recipient,
            address,
            shipment_type,
            status,
        )

        if success:
            self.refresh()

        return success, message

    def lookup_postal_code(
            self,
            postal_code: str,
    ) -> dict[str, str]:
        """Consulta un código postal a través del servicio."""

        return self.controller.get_location_by_postal_code(
            postal_code
        )

