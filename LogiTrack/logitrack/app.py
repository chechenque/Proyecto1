import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    """Ventana principal de LogiTrack Desktop."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("LogiTrack Desktop")
        self.resize(1100, 700)

        self.shipments: list[dict[str, str]] = []

        self._create_ui()

    def _create_ui(self) -> None:
        """Construye la interfaz principal."""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # =========================================================
        # ENCABEZADO
        # =========================================================

        header_layout = QHBoxLayout()

        title = QLabel("LogiTrack Desktop")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )

        subtitle = QLabel("Gestión de envíos")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignRight)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(subtitle)

        main_layout.addLayout(header_layout)

        # =========================================================
        # CONTENIDO PRINCIPAL
        # =========================================================

        content_layout = QHBoxLayout()

        # ---------------------------------------------------------
        # TABLA
        # ---------------------------------------------------------

        self.shipment_table = QTableWidget()

        self.shipment_table.setColumnCount(4)
        self.shipment_table.setHorizontalHeaderLabels(
            [
                "Destinatario",
                "Dirección",
                "Tipo",
                "Estado",
            ]
        )

        self.shipment_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.shipment_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        content_layout.addWidget(self.shipment_table, stretch=3)

        # ---------------------------------------------------------
        # FORMULARIO
        # ---------------------------------------------------------

        form_group = QGroupBox("Nuevo envío")
        form_layout = QFormLayout()

        self.recipient_input = QLineEdit()
        self.recipient_input.setPlaceholderText(
            "Nombre del destinatario"
        )

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText(
            "Dirección de entrega"
        )

        self.type_combo = QComboBox()
        self.type_combo.addItems(
            [
                "Paquete",
                "Documento",
                "Carga",
            ]
        )

        self.status_combo = QComboBox()
        self.status_combo.addItems(
            [
                "Pendiente",
                "En ruta",
                "Entregado",
                "Retrasado",
            ]
        )

        form_layout.addRow(
            "Destinatario:",
            self.recipient_input,
        )

        form_layout.addRow(
            "Dirección:",
            self.address_input,
        )

        form_layout.addRow(
            "Tipo:",
            self.type_combo,
        )

        form_layout.addRow(
            "Estado:",
            self.status_combo,
        )

        # ---------------------------------------------------------
        # BOTONES
        # ---------------------------------------------------------

        buttons_layout = QHBoxLayout()

        save_button = QPushButton("Guardar")
        clear_button = QPushButton("Limpiar")
        search_button = QPushButton("Buscar")

        save_button.clicked.connect(self._save_shipment)
        clear_button.clicked.connect(self._clear_form)
        search_button.clicked.connect(self._search_shipments)

        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(clear_button)
        buttons_layout.addWidget(search_button)

        form_layout.addRow(buttons_layout)

        form_group.setLayout(form_layout)

        content_layout.addWidget(form_group, stretch=1)

        main_layout.addLayout(content_layout)

        # =========================================================
        # BARRA DE ESTADO
        # =========================================================

        self.statusBar().showMessage(
            "Listo • 0 envíos registrados"
        )

    def _save_shipment(self) -> None:
        """Registra un envío temporalmente en memoria."""

        recipient = self.recipient_input.text().strip()
        address = self.address_input.text().strip()

        if not recipient:
            self.statusBar().showMessage(
                "Error: el destinatario es obligatorio."
            )
            self.recipient_input.setFocus()
            return

        if not address:
            self.statusBar().showMessage(
                "Error: la dirección es obligatoria."
            )
            self.address_input.setFocus()
            return

        shipment = {
            "recipient": recipient,
            "address": address,
            "type": self.type_combo.currentText(),
            "status": self.status_combo.currentText(),
        }

        self.shipments.append(shipment)

        self._refresh_table()
        self._clear_form()

        self.statusBar().showMessage(
            f"Envío registrado correctamente • "
            f"{len(self.shipments)} envío(s)"
        )

    def _clear_form(self) -> None:
        """Limpia el formulario."""

        self.recipient_input.clear()
        self.address_input.clear()

        self.type_combo.setCurrentIndex(0)
        self.status_combo.setCurrentIndex(0)

        self.recipient_input.setFocus()

    def _search_shipments(self) -> None:
        """Busca envíos por destinatario o dirección."""

        search_text = self.recipient_input.text().strip().lower()

        if not search_text:
            self._refresh_table()
            return

        filtered = [
            shipment
            for shipment in self.shipments
            if search_text in shipment["recipient"].lower()
            or search_text in shipment["address"].lower()
        ]

        self._refresh_table(filtered)

        self.statusBar().showMessage(
            f"{len(filtered)} resultado(s) encontrado(s)"
        )

    def _refresh_table(
        self,
        shipments: list[dict[str, str]] | None = None,
    ) -> None:
        """Actualiza la tabla con los envíos disponibles."""

        data = (
            self.shipments
            if shipments is None
            else shipments
        )

        self.shipment_table.setRowCount(len(data))

        for row, shipment in enumerate(data):
            self.shipment_table.setItem(
                row,
                0,
                QTableWidgetItem(shipment["recipient"]),
            )

            self.shipment_table.setItem(
                row,
                1,
                QTableWidgetItem(shipment["address"]),
            )

            self.shipment_table.setItem(
                row,
                2,
                QTableWidgetItem(shipment["type"]),
            )

            self.shipment_table.setItem(
                row,
                3,
                QTableWidgetItem(shipment["status"]),
            )


def run() -> None:
    """Inicia la aplicación."""

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())