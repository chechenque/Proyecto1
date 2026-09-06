LIGHT_THEME = """
QMainWindow {
    background-color: #f5f6f8;
}

QLabel {
    color: #202124;
}

QGroupBox {
    font-weight: bold;
    border: 1px solid #d9dce1;
    border-radius: 6px;
    margin-top: 10px;
    padding: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QLineEdit,
QComboBox {
    min-height: 32px;
    border: 1px solid #c7cbd1;
    border-radius: 5px;
    padding: 4px 8px;
    background-color: white;
    color: #202124;
}

QComboBox QAbstractItemView {
    background-color: white;
    color: #202124;
    selection-background-color: #dfe7fd;
    selection-color: #202124;
}

QPushButton {
    min-height: 34px;
    padding: 5px 14px;
    background-color: #ffffff;
    color: #202124;
    border: 1px solid #c7cbd1;
    border-radius: 6px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #f0f2f5;
}

QPushButton:pressed {
    background-color: #e2e5e9;
}

QPushButton:disabled {
    color: #9aa0a6;
    background-color: #f1f3f4;
}

QTableView {
    background-color: #ffffff;
    alternate-background-color: #f8f9fa;
    gridline-color: #e0e3e7;
    color: #202124;
    selection-background-color: #dfe7fd;
    selection-color: #202124;
}


QHeaderView::section {
    padding: 6px;
    font-weight: bold;
    background-color: #f1f3f4;
    color: #202124;
    border: 1px solid #d9dce1;
}
"""


DARK_THEME = """
QMainWindow {
    background-color: #202124;
}



QLabel {
    color: #e8eaed;
}

QGroupBox {
    font-weight: bold;
    border: 1px solid #5f6368;
    border-radius: 6px;
    margin-top: 10px;
    padding: 10px;
    color: #e8eaed;
    background-color: #202124;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QLineEdit,
QComboBox {
    min-height: 32px;
    border: 1px solid #5f6368;
    border-radius: 5px;
    padding: 4px 8px;
    background-color: #303134;
    color: #e8eaed;
}

QLineEdit:focus,
QComboBox:focus {
    border: 1px solid #8ab4f8;
}

QPushButton {
    min-height: 32px;
    padding: 4px 12px;
    background-color: #3c4043;
    color: #e8eaed;
    border: 1px solid #5f6368;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #4a4d51;
}

QPushButton:pressed {
    background-color: #5f6368;
}

QTableView {
    background-color: #303134;
    alternate-background-color: #292a2d;
    gridline-color: #5f6368;
    color: #e8eaed;
}

QHeaderView::section {
    padding: 6px;
    font-weight: bold;
    background-color: #3c4043;
    color: #e8eaed;
}
"""


def get_theme(dark: bool = False) -> str:
    """Devuelve el tema visual seleccionado."""
    return DARK_THEME if dark else LIGHT_THEME