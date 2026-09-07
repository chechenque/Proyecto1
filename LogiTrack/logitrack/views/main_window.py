from PyQt6.QtCore import Qt, QThread
from logitrack.ui.theme import get_theme
from logitrack.services.worker import ShipmentWorker
from PyQt6.QtWidgets import (
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
    QApplication,
)


class MainWindow(QMainWindow):
    """Ventana principal de LogiTrack Desktop."""

    def __init__(self, controller, view_model) -> None:
        super().__init__()

        self.setWindowTitle("LogiTrack Desktop")
        self.resize(1100, 700)

        self.controller = controller
        self.view_model = view_model

        self._create_ui()

        self.shipment_table.setModel(
            self.view_model.shipment_model
        )

    def _create_ui(self) -> None:
        """Construye la interfaz principal."""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # HEADER
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)

        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)

        title = QLabel("LogiTrack Desktop")
        subtitle = QLabel("Gestión de envíos")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignRight)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(subtitle)

        header_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        main_layout.addWidget(header_widget)

        # CONTENT
        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.shipment_table = QTableView()

        self.shipment_table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.shipment_table.setEditTriggers(
            QTableView.EditTrigger.NoEditTriggers
        )

        self.shipment_table.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )

        self.shipment_table.setSortingEnabled(True)
        self.shipment_table.setAlternatingRowColors(True)

        header = self.shipment_table.horizontalHeader()
        header.setStretchLastSection(True)

        for column in range(4):
            header.setSectionResizeMode(

                column,

                header.ResizeMode.Stretch,

            )

        splitter.addWidget(self.shipment_table)

        # FORM
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
            ["Paquete", "Documento", "Carga"]
        )

        self.status_combo = QComboBox()
        self.status_combo.addItems(
            ["Pendiente", "En ruta", "Entregado", "Retrasado"]
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

        buttons_layout = QHBoxLayout()

        self.save_button = QPushButton("Guardar")
        self.clear_button = QPushButton("Limpiar")
        self.search_button = QPushButton("Buscar")
        self.async_button = QPushButton(
            "Probar tarea asíncrona"
        )
        self.theme_button = QPushButton("🌙 Modo oscuro")
        self.theme_button.setCheckable(True)

        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.search_button)

        form_layout.addRow(buttons_layout)
        form_layout.addRow(self.async_button)
        form_layout.addRow(self.theme_button)

        form_group.setLayout(form_layout)

        form_group.setMinimumWidth(300)
        form_group.setMaximumWidth(400)

        form_group.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
        )

        splitter.addWidget(form_group)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)

        splitter.setSizes([800, 300])

        main_layout.addWidget(splitter)

        self.statusBar().showMessage(
            "Listo • 0 envíos registrados"
        )
        self.save_button.clicked.connect(self._save_shipment)
        self.search_button.clicked.connect(self._search_shipments)
        self.clear_button.clicked.connect(self._clear_form)
        self.theme_button.toggled.connect(self._toggle_theme)
        self.async_button.clicked.connect(

            self._start_async_operation

        )

    def _save_shipment(self) -> None:
        """Solicita al ViewModel la creación de un envío."""

        success, message = self.view_model.create_shipment(
            self.recipient_input.text(),
            self.address_input.text(),
            self.type_combo.currentText(),
            self.status_combo.currentText(),
        )

        if not success:
            self.statusBar().showMessage(
                f"Error: {message}"
            )

            if not self.recipient_input.text().strip():
                self.recipient_input.setFocus()
            else:
                self.address_input.setFocus()

            return

        self.recipient_input.clear()
        self.address_input.clear()

        self.statusBar().showMessage(
            f"{message} • "
            f"{self.view_model.count()} envío(s)"
        )

    def _search_shipments(self) -> None:
        """Solicita al ViewModel la búsqueda de envíos."""

        recipient_text = self.recipient_input.text().strip()
        address_text = self.address_input.text().strip()

        search_text = recipient_text or address_text

        result_count = self.view_model.search(
            search_text
        )

        if search_text:
            self.statusBar().showMessage(
                f"{result_count} resultado(s) encontrado(s)"
            )
        else:
            self.statusBar().showMessage(
                f"{result_count} envío(s) registrado(s)"
            )

    def _clear_form(self) -> None:
        """Limpia los campos del formulario."""

        self.recipient_input.clear()
        self.address_input.clear()

        self.type_combo.setCurrentIndex(0)
        self.status_combo.setCurrentIndex(0)

        self.view_model.refresh()

        self.recipient_input.setFocus()

        self.statusBar().showMessage(
            f"Listo • "
            f"{self.view_model.count()} envío(s) registrado(s)"
        )

    def _toggle_theme(self, checked: bool) -> None:
        """Cambia entre el tema claro y oscuro."""

        app = QApplication.instance()

        if app is None:
            return

        app.setStyleSheet(
            get_theme(dark=checked)
        )

        if checked:
            self.theme_button.setText("☀️ Modo claro")
        else:
            self.theme_button.setText("🌙 Modo oscuro")

    def _start_async_operation(self) -> None:
        """Inicia una operación larga sin bloquear la interfaz."""

        self.statusBar().showMessage(
            "Procesando..."
        )

        self.async_button.setEnabled(False)

        self.async_thread = QThread()
        self.async_worker = ShipmentWorker(
            self.controller.get_service()
        )

        self.async_worker.moveToThread(
            self.async_thread
        )

        self.async_thread.started.connect(
            self.async_worker.run
        )

        self.async_worker.finished.connect(
            self._async_operation_finished
        )

        self.async_worker.error.connect(
            self._async_operation_error
        )

        self.async_worker.finished.connect(
            self.async_thread.quit
        )

        self.async_worker.error.connect(
            self.async_thread.quit
        )

        self.async_thread.finished.connect(
            self.async_worker.deleteLater
        )

        self.async_thread.finished.connect(
            self.async_thread.deleteLater
        )

        self.async_thread.start()

    def _async_operation_finished(
            self,
            message: str,
    ) -> None:
        """Muestra el resultado de una operacfión asíncrona."""
        self.async_button.setEnabled(True)
        self.statusBar().showMessage(message)

    def _async_operation_error(
            self,
            message: str,
    ) -> None:
        """Muestra un error de una operación asíncrona."""
        self.async_button.setEnabled(True)
        self.statusBar().showMessage(
            f"Error: {message}"
        )