from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QButtonGroup,
    QPushButton,
    QFrame,
)


class Sidebar(QFrame):
    nav_clicked = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")
        self.setFixedWidth(240)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 12)
        layout.setSpacing(4)

        brand = QLabel("Kora")
        brand.setObjectName("brand")
        layout.addWidget(brand)
        layout.addSpacing(8)

        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        for name in ("Home", "Search", "Library"):
            btn = QPushButton(f"   {name}")
            btn.setObjectName("navButton")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            self.group.addButton(btn)
            layout.addWidget(btn)
            btn.clicked.connect(lambda _c, n=name: self.nav_clicked.emit(n))

        layout.addStretch()
