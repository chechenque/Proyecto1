import sys

from PyQt6.QtCore import Qt
from PyQt6.QtCore import QThread

from logitrack.controllers.shipment_view_model import ShipmentViewModel
from logitrack.services.shipment_service import ShipmentService
from logitrack.services.worker import ShipmentWorker
from logitrack.models.shipment_table_model import ShipmentTableModel
from logitrack.controllers.shipment_controller import ShipmentController
from logitrack.views.main_window import MainWindow
from logitrack.ui.theme import get_theme
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QPushButton,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QTableView,
    QVBoxLayout,
    QWidget,
)



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

    window = MainWindow(
        controller,
        view_model,
    )
    window.show()

    sys.exit(app.exec())