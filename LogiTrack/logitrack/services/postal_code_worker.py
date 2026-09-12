from collections.abc import Callable

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class PostalCodeWorker(QObject):
    """Consulta códigos postales fuera del hilo de la interfaz."""

    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(
        self,
        postal_code: str,
        lookup: Callable[[str], dict[str, str]],
    ) -> None:
        super().__init__()
        self.postal_code = postal_code
        self.lookup = lookup

    @pyqtSlot()
    def run(self) -> None:
        """Ejecuta la consulta del código postal."""

        try:
            result = self.lookup(self.postal_code)
            self.finished.emit(result)
        except Exception as exc:
            self.error.emit(str(exc))