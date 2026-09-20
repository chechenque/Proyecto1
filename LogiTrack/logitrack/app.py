import sys

from PyQt6.QtWidgets import (
    QApplication,
)

from logitrack.controllers.offline_operation_controller import (
    OfflineOperationController,
)
from logitrack.controllers.offline_operation_view_model import (
    OfflineOperationViewModel,
)
from logitrack.controllers.shipment_controller import ShipmentController
from logitrack.controllers.shipment_view_model import ShipmentViewModel
from logitrack.models.shipment_table_model import ShipmentTableModel
from logitrack.ui.theme import get_theme
from logitrack.views.main_window import MainWindow


def run() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(get_theme())

    controller = ShipmentController()

    shipment_model = ShipmentTableModel(
        controller.get_shipments()
    )

    view_model = ShipmentViewModel(

        controller,

        shipment_model,

    )

    offline_controller = OfflineOperationController()

    offline_view_model = OfflineOperationViewModel(
        offline_controller,
    )

    window = MainWindow(
        controller,
        view_model,
        offline_view_model,
    )

    window.show()

    sys.exit(app.exec())