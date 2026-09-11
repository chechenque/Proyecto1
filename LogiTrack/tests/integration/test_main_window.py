import pytest
from PyQt6.QtWidgets import QApplication

from logitrack.controllers.shipment_controller import (
    ShipmentController,
)
from logitrack.controllers.shipment_view_model import (
    ShipmentViewModel,
)
from logitrack.models.shipment_table_model import (
    ShipmentTableModel,
)
from logitrack.services.shipment_service import (
    ShipmentService,
)
from logitrack.views.main_window import MainWindow


@pytest.fixture
def qapp() -> QApplication:
    """Proporciona una instancia de QApplication para los tests."""

    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    return app


def create_window(
    tmp_path,
    qapp: QApplication,
) -> MainWindow:
    """Crea una ventana utilizando una base temporal."""

    service = ShipmentService(
        tmp_path / "test.db"
    )

    controller = ShipmentController(service)

    model = ShipmentTableModel(
        controller.get_shipments()
    )

    view_model = ShipmentViewModel(
        controller,
        model,
    )

    return MainWindow(
        controller,
        view_model,
    )


def test_main_window_initializes(
    tmp_path,
    qapp: QApplication,
) -> None:
    """La ventana debe inicializarse correctamente."""

    window = create_window(
        tmp_path,
        qapp,
    )

    assert window.windowTitle() == "LogiTrack Desktop"
    assert window.shipment_table is not None
    assert window.recipient_input is not None
    assert window.address_input is not None
    assert window.type_combo is not None
    assert window.status_combo is not None

    window.close()

def test_main_window_saves_shipment(
    tmp_path,
    qapp: QApplication,
) -> None:
    """La ventana debe guardar un envío correctamente."""

    window = create_window(
        tmp_path,
        qapp,
    )

    window.recipient_input.setText("Ana López")
    window.address_input.setText("Av. Reforma 123")

    window.type_combo.setCurrentText("Nacional")
    window.status_combo.setCurrentText("Pendiente")

    window._save_shipment()

    assert window.view_model.count() == 1
    assert (
        window.view_model.shipment_model.shipments[0]["recipient"]
        == "Ana López"
    )

    assert window.recipient_input.text() == ""
    assert window.address_input.text() == ""

    window.close()

def test_main_window_rejects_empty_recipient(
    tmp_path,
    qapp: QApplication,
) -> None:
    """La ventana debe rechazar un envío sin destinatario."""

    window = create_window(
        tmp_path,
        qapp,
    )

    window.address_input.setText("Av. Reforma 123")

    window._save_shipment()

    assert window.view_model.count() == 0
    assert "obligatorio" in window.statusBar().currentMessage()

    window.close()

def test_main_window_rejects_empty_address(
    tmp_path,
    qapp: QApplication,
) -> None:
    """La ventana debe rechazar un envío sin dirección."""

    window = create_window(
        tmp_path,
        qapp,
    )

    window.recipient_input.setText("Ana López")

    window._save_shipment()

    assert window.view_model.count() == 0
    assert "obligatoria" in window.statusBar().currentMessage()

    window.close()

def test_main_window_searches_shipments(
    tmp_path,
    qapp: QApplication,
) -> None:
    """La ventana debe buscar envíos por destinatario."""

    window = create_window(
        tmp_path,
        qapp,
    )

    window.recipient_input.setText("Ana López")
    window.address_input.setText("Av. Reforma 123")

    window._save_shipment()

    window.recipient_input.setText("Ana")

    window._search_shipments()

    assert window.view_model.shipment_model.rowCount() == 1
    assert (
        window.view_model.shipment_model.shipments[0]["recipient"]
        == "Ana López"
    )
    assert "1 resultado" in window.statusBar().currentMessage()

    window.close()

def test_main_window_clears_form(
    tmp_path,
    qapp: QApplication,
) -> None:
    """La ventana debe limpiar el formulario correctamente."""

    window = create_window(
        tmp_path,
        qapp,
    )

    window.recipient_input.setText("Ana López")
    window.address_input.setText("Av. Reforma 123")

    window.type_combo.setCurrentIndex(1)
    window.status_combo.setCurrentIndex(1)

    window._clear_form()

    assert window.recipient_input.text() == ""
    assert window.address_input.text() == ""
    assert window.type_combo.currentIndex() == 0
    assert window.status_combo.currentIndex() == 0

    window.close()

def test_main_window_searches_all_when_search_is_empty(
    tmp_path,
    qapp: QApplication,
) -> None:
    """La búsqueda vacía debe mostrar todos los envíos."""

    window = create_window(
        tmp_path,
        qapp,
    )

    window.recipient_input.setText("Ana López")
    window.address_input.setText("Av. Reforma 123")
    window._save_shipment()

    window.recipient_input.setText("")

    window._search_shipments()

    assert window.view_model.shipment_model.rowCount() == 1
    assert (
        "1 envío(s) registrado(s)"
        in window.statusBar().currentMessage()
    )

    window.close()

def test_main_window_toggles_theme(
    tmp_path,
    qapp: QApplication,
) -> None:
    """La ventana debe cambiar entre tema claro y oscuro."""

    window = create_window(
        tmp_path,
        qapp,
    )

    assert window.theme_button.isChecked() is False
    assert window.theme_button.text() == "🌙 Modo oscuro"

    window.theme_button.setChecked(True)

    assert window.theme_button.isChecked() is True
    assert window.theme_button.text() == "☀️ Modo claro"

    window.theme_button.setChecked(False)

    assert window.theme_button.isChecked() is False
    assert window.theme_button.text() == "🌙 Modo oscuro"

    window.close()

def test_main_window_starts_async_operation(
    tmp_path,
    qapp: QApplication,
) -> None:
    """La ventana debe iniciar una operación asíncrona."""

    window = create_window(
        tmp_path,
        qapp,
    )

    window._start_async_operation()

    assert window.async_button.isEnabled() is False
    assert window.statusBar().currentMessage() == "Procesando..."

    window.async_thread.quit()
    window.async_thread.wait()

    window.close()

def test_main_window_async_operation_finished(
    tmp_path,
    qapp: QApplication,
) -> None:
    """La ventana debe mostrar el resultado de una operación exitosa."""

    window = create_window(
        tmp_path,
        qapp,
    )

    window.async_button.setEnabled(False)

    window._async_operation_finished(
        "Operación completada correctamente."
    )

    assert window.async_button.isEnabled() is True
    assert (
        window.statusBar().currentMessage()
        == "Operación completada correctamente."
    )

    window.close()


def test_main_window_async_operation_error(
    tmp_path,
    qapp: QApplication,
) -> None:
    """La ventana debe mostrar el error de una operación."""

    window = create_window(
        tmp_path,
        qapp,
    )

    window.async_button.setEnabled(False)

    window._async_operation_error(
        "Error de conexión"
    )

    assert window.async_button.isEnabled() is True
    assert (
        window.statusBar().currentMessage()
        == "Error: Error de conexión"
    )

    window.close()