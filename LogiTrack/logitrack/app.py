import sys

from PyQt6.QtCore import Qt
from PyQt6.QtCore import QThread
from logitrack.services.shipment_service import ShipmentService
from logitrack.services.worker import ShipmentWorker
from logitrack.models.shipment_table_model import ShipmentTableModel
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

        # HEADER
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)

        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)

        title = QLabel("LogiTrack Desktop")
        subtitle = QLabel("Gestión de envíos")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.theme_button = QPushButton("🌙 Modo oscuro")
        self.theme_button.setCheckable(True)
        self.theme_button.toggled.connect(self._toggle_theme)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(subtitle)
        header_layout.addWidget(self.theme_button)

        header_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        main_layout.addWidget(header_widget)

        # =========================================================
        # CONTENIDO PRINCIPAL
        # =========================================================

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # ---------------------------------------------------------
        # TABLA
        # ---------------------------------------------------------

        self.shipment_table = QTableView()

        self.shipment_model = ShipmentTableModel(self.shipments)
        self.shipment_table.setModel(self.shipment_model)

        self.shipment_table.setEditTriggers(
            QTableView.EditTrigger.NoEditTriggers
        )

        self.shipment_table.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )
        self.shipment_table.setSortingEnabled(True)
        self.shipment_table.setAlternatingRowColors(True)

        self.shipment_table.horizontalHeader().setStretchLastSection(True)

        header = self.shipment_table.horizontalHeader()
        header.setSectionResizeMode(
            0,
            header.ResizeMode.Stretch,
        )
        header.setSectionResizeMode(
            1,
            header.ResizeMode.Stretch,
        )
        header.setSectionResizeMode(
            2,
            header.ResizeMode.ResizeToContents,
        )
        header.setSectionResizeMode(
            3,
            header.ResizeMode.ResizeToContents,
        )

        self.shipment_table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )


        # ---------------------------------------------------------
        # FORMULARIO
        # ---------------------------------------------------------

        form_group = QGroupBox("Nuevo envío")
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(12)
        form_layout.setHorizontalSpacing(10)

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
        async_button = QPushButton("Probar tarea asíncrona")

        save_button.clicked.connect(self._save_shipment)
        clear_button.clicked.connect(self._clear_form)
        search_button.clicked.connect(self._search_shipments)
        async_button.clicked.connect(self._start_async_operation)

        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(clear_button)
        buttons_layout.addWidget(search_button)
        buttons_layout.addWidget(async_button)

        form_layout.addRow(buttons_layout)

        form_group.setLayout(form_layout)

        form_group.setMinimumWidth(300)
        form_group.setMaximumWidth(400)
        form_group.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
        )

        splitter.addWidget(self.shipment_table)
        splitter.addWidget(form_group)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)

        # =========================================================
        # BARRA DE ESTADO
        # =========================================================

        self.statusBar().showMessage(
            "Listo • 0 envíos registrados"
        )

    def _toggle_theme(self, checked: bool) -> None:
        """Cambia entre el tema claro y oscuro."""
        app = QApplication.instance()

        if app is not None:
            app.setStyleSheet(get_theme(dark=checked))

        if checked:
            self.theme_button.setText("☀️ Modo claro")
        else:
            self.theme_button.setText("🌙 Modo oscuro")

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

    def _start_async_operation(self) -> None:
        """Inicia una operación larga sin bloquear la interfaz."""
        self.statusBar().showMessage("Procesando...")

        self.async_thread = QThread()
        self.async_worker = ShipmentWorker(ShipmentService())

        self.async_worker.moveToThread(self.async_thread)

        self.async_thread.started.connect(self.async_worker.run)
        self.async_worker.finished.connect(self._async_operation_finished)
        self.async_worker.error.connect(self._async_operation_error)

        self.async_worker.finished.connect(self.async_thread.quit)
        self.async_worker.error.connect(self.async_thread.quit)

        self.async_thread.finished.connect(self.async_worker.deleteLater)
        self.async_thread.finished.connect(self.async_thread.deleteLater)

        self.async_thread.start()

    def _async_operation_finished(self, message: str) -> None:
        """Procesa el resultado de una operación exitosa."""
        self.statusBar().showMessage(message)

    def _async_operation_error(self, message: str) -> None:
        """Procesa un error de la operación asíncrona."""
        self.statusBar().showMessage(f"Error: {message}")

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
        data = self.shipments if shipments is None else shipments

        self.shipment_model.update_shipments(data)


def run() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(get_theme())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())