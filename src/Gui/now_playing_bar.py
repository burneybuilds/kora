from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QFrame,
)


class NowPlayingBar(QFrame):
    play_pause_clicked = Signal()
    next_clicked = Signal()
    prev_clicked = Signal()
    volume_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.setObjectName("nowPlayingBar")
        self.setFixedHeight(88)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 24, 8)
        layout.setSpacing(12)

        info_box = QVBoxLayout()
        info_box.setSpacing(2)
        self.title = QLabel("No track playing")
        self.title.setObjectName("nowPlayingMeta")
        self.title.setStyleSheet("color: #FFFFFF; font-weight: bold; font-size: 14px;")
        self.meta = QLabel("")
        self.meta.setObjectName("nowPlayingMeta")
        info_box.addWidget(self.title)
        info_box.addWidget(self.meta)
        info_box.addStretch()
        left = QWidget()
        left.setFixedWidth(260)
        left.setLayout(info_box)
        layout.addWidget(left)

        layout.addStretch()

        center = QWidget()
        center_layout = QHBoxLayout(center)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(8)
        center_layout.setAlignment(Qt.AlignCenter)

        self.shuffle = self._control_btn("images/suffel.svg")
        self.prev = self._control_btn("images/previous.svg")
        self.play_pause = QPushButton()
        self.play_pause.setObjectName("playButton")
        self.play_pause.setFixedSize(40, 40)
        self.play_pause.setIcon(QIcon("images/play.svg"))
        self.play_pause.setIconSize(QSize(16, 16))
        self.play_pause.setCursor(Qt.PointingHandCursor)
        self.next = self._control_btn("images/next.svg")
        self.repeat = self._control_btn("images/repeat.svg")

        for w in (self.shuffle, self.prev, self.play_pause, self.next, self.repeat):
            center_layout.addWidget(w)

        layout.addWidget(center)
        layout.addStretch()

        right = QWidget()
        right_layout = QHBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)
        right_layout.setAlignment(Qt.AlignRight)

        self.volume_icon = QLabel()
        self.volume_icon.setPixmap(QIcon("images/volume.svg").pixmap(16, 16))
        right_layout.addWidget(self.volume_icon)

        self.volume = QSlider(Qt.Horizontal)
        self.volume.setRange(0, 100)
        self.volume.setValue(100)
        self.volume.setFixedWidth(120)
        right_layout.addWidget(self.volume)
        right.setFixedWidth(180)
        layout.addWidget(right)

        self.play_pause.clicked.connect(self.play_pause_clicked.emit)
        self.next.clicked.connect(self.next_clicked.emit)
        self.prev.clicked.connect(self.prev_clicked.emit)
        self.volume.valueChanged.connect(self.volume_changed.emit)

        self._is_playing = False

    def _control_btn(self, path):
        btn = QPushButton()
        btn.setObjectName("controlButton")
        btn.setFixedSize(32, 32)
        btn.setIcon(QIcon(path))
        btn.setIconSize(QSize(14, 14))
        btn.setCursor(Qt.PointingHandCursor)
        return btn

    def set_track_title(self, text):
        self.title.setText(text)

    def set_playing_state(self, is_playing):
        self._is_playing = is_playing
        icon = "images/pause.svg" if is_playing else "images/play.svg"
        self.play_pause.setIcon(QIcon(icon))

    def set_volume_icon(self, muted=False):
        path = "images/previous.svg" if muted else "images/volume.svg"
        self.volume_icon.setPixmap(QIcon(path).pixmap(16, 16))
