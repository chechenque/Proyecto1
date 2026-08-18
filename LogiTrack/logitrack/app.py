import sys

from PyQt6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    """Ventana principal de LogiTrack Desktop."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("LogiTrack Desktop")
        self.resize(1000, 650)


def run() -> None:
    """Inicia la aplicación."""
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())