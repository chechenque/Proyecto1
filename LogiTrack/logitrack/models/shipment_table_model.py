from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtGui import QColor

class ShipmentTableModel(QAbstractTableModel):
    """Modelo de datos para la tabla de envíos."""

    HEADERS = [
        "Destinatario",
        "Dirección",
        "Tipo",
        "Estado",
    ]

    def __init__(
        self,
        shipments: list[dict[str, str]] | None = None,
    ) -> None:
        super().__init__()
        self.shipments = shipments or []

    def rowCount(
        self,
        parent: QModelIndex = QModelIndex(),
    ) -> int:
        """Devuelve el número de filas."""
        if parent.isValid():
            return 0

        return len(self.shipments)

    def columnCount(
        self,
        parent: QModelIndex = QModelIndex(),
    ) -> int:
        """Devuelve el número de columnas."""
        if parent.isValid():
            return 0

        return len(self.HEADERS)

    def data(
            self,
            index: QModelIndex,
            role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | QColor | None:
        """Devuelve el dato solicitado por la vista."""
        if not index.isValid():
            return None

        shipment = self.shipments[index.row()]

        values = [
            shipment["recipient"],
            shipment["address"],
            shipment["type"],
            shipment["status"],
        ]

        if role == Qt.ItemDataRole.DisplayRole:
            return values[index.column()]

        if role == Qt.ItemDataRole.ForegroundRole:
            status = shipment["status"]

            if status == "Entregado":
                return QColor("#188038")

            if status == "En ruta":
                return QColor("#1967d2")

            if status == "Retrasado":
                return QColor("#d93025")

            if status == "Pendiente":
                return QColor("#b06000")

        if role == Qt.ItemDataRole.BackgroundRole:
            if index.column() != 3:
                return None

            status = shipment["status"]

            if status == "Entregado":
                return QColor("#e6f4ea")

            if status == "En ruta":
                return QColor("#e8f0fe")

            if status == "Retrasado":
                return QColor("#fce8e6")

            if status == "Pendiente":
                return QColor("#fef7e0")

        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        """Devuelve los encabezados de la tabla."""
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]

        return str(section + 1)

    def update_shipments(
        self,
        shipments: list[dict[str, str]],
    ) -> None:
        """Actualiza los datos del modelo."""
        self.beginResetModel()
        self.shipments = shipments
        self.endResetModel()

    def sort(
        self,
        column: int,
        order: Qt.SortOrder = Qt.SortOrder.AscendingOrder,
    ) -> None:
        """Ordena los envíos por la columna seleccionada."""

        self.layoutAboutToBeChanged.emit()

        keys = [
            "recipient",
            "address",
            "type",
            "status",
        ]

        key = keys[column]

        self.shipments.sort(
            key=lambda shipment: shipment[key].lower(),
            reverse=order == Qt.SortOrder.DescendingOrder,
        )

        self.layoutChanged.emit()