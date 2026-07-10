from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSlider


class ControlsWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        next_icon = QIcon("images//next.svg")
        next = QPushButton(next_icon, "")

        play_icon = QIcon("images//play.svg")
        play = QPushButton(play_icon, "")

        repeat_icon = QIcon("images//repeat.svg")
        repeat = QPushButton(repeat_icon, "")

        previous_icon = QIcon("images//previous.svg")
        previous = QPushButton(previous_icon, "")

        shuffle_icon = QIcon("images//suffel.svg")
        shuffle = QPushButton(shuffle_icon, "")

        volume = QSlider(Qt.Horizontal)
        volume.setRange(0, 100)   
        volume.setValue(100) 

        layout.addWidget(shuffle)
        layout.addWidget(previous)
        layout.addWidget(play)
        layout.addWidget(next)
        layout.addWidget(repeat)
        layout.addWidget(volume)