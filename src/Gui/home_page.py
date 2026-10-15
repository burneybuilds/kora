import os

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMenu,
)


class HomePage(QWidget):
    track_selected = Signal(int)
    remove_requested = Signal(int)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        header_row = QHBoxLayout()
        title = QLabel("Your Library")
        title.setObjectName("pageTitle")
        header_row.addWidget(title)
        header_row.addStretch()
        layout.addLayout(header_row)

        self.subtitle = QLabel("Scanning your music...")
        self.subtitle.setObjectName("trackMeta")
        layout.addWidget(self.subtitle)

        self.list = QListWidget()
        self.list.itemClicked.connect(self._on_item_clicked)
        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self._on_context_menu)
        layout.addWidget(self.list, 1)

    def _on_item_clicked(self, item: QListWidgetItem):
        self.track_selected.emit(item.data(Qt.UserRole))

    def _on_context_menu(self, pos):
        item = self.list.itemAt(pos)
        if item is None:
            return
        menu = QMenu(self)
        remove_action = menu.addAction("Remove from Library")
        if menu.exec(self.list.mapToGlobal(pos)) == remove_action:
            self.remove_requested.emit(item.data(Qt.UserRole))

    def set_tracks(self, tracks):
        self.list.clear()
        for i, path in enumerate(tracks):
            name = os.path.splitext(os.path.basename(path))[0]
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, i)
            item.setToolTip(path)
            self.list.addItem(item)
        if tracks:
            self.subtitle.setText(f"{len(tracks)} tracks in your library")
        else:
            self.subtitle.setText("No music found in your Music folder.")

    def highlight_current(self, index):
        if 0 <= index < self.list.count():
            self.list.setCurrentRow(index)
