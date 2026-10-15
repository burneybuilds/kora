from PySide6.QtGui import QColor, QPalette, QFont
from PySide6.QtCore import Qt

BG = "#121212"
BG_LIGHT = "#181818"
BG_LIGHTER = "#282828"
SIDEBAR_BG = "#000000"
GREEN = "#1DB954"
GREEN_HOVER = "#1ED760"
TEXT = "#FFFFFF"
TEXT_SECONDARY = "#B3B3B3"
HIGHLIGHT = "#1DB954"

SPOTIFY_QSS = """
QWidget {
    background-color: %(BG)s;
    color: %(TEXT)s;
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 14px;
}

QMainWindow {
    background-color: %(BG)s;
}

QFrame#sidebar {
    background-color: %(SIDEBAR_BG)s;
}

QPushButton#navButton {
    background: transparent;
    border: none;
    color: %(TEXT_SECONDARY)s;
    text-align: left;
    padding: 12px 20px;
    font-size: 15px;
    font-weight: bold;
    border-radius: 8px;
}

QPushButton#navButton:hover {
    color: %(TEXT)s;
    background-color: %(BG_LIGHT)s;
}

QPushButton#navButton:checked {
    color: %(TEXT)s;
    background-color: %(BG_LIGHTER)s;
}

QLabel#brand {
    color: %(TEXT)s;
    font-size: 22px;
    font-weight: bold;
    padding: 20px;
}

QLabel#pageTitle {
    color: %(TEXT)s;
    font-size: 28px;
    font-weight: bold;
}

QLabel#sectionHeader {
    color: %(TEXT)s;
    font-size: 20px;
    font-weight: bold;
}

QLabel#trackTitle {
    color: %(TEXT)s;
    font-size: 14px;
    font-weight: bold;
}

QLabel#trackMeta, QLabel#nowPlayingMeta {
    color: %(TEXT_SECONDARY)s;
    font-size: 12px;
}

QFrame#nowPlayingBar {
    background-color: %(BG_LIGHT)s;
    border-top: 1px solid %(BG_LIGHTER)s;
}

QListWidget {
    background-color: %(BG)s;
    border: none;
    outline: none;
    padding: 4px;
}

QListWidget::item {
    background-color: transparent;
    border-radius: 6px;
    padding: 8px;
    margin: 2px 0px;
    color: %(TEXT)s;
}

QListWidget::item:hover {
    background-color: %(BG_LIGHT)s;
}

QListWidget::item:selected {
    background-color: %(BG_LIGHTER)s;
}

QPushButton#controlButton {
    background: transparent;
    border: none;
    border-radius: 16px;
    padding: 4px;
}

QPushButton#controlButton:hover {
    background-color: %(BG_LIGHTER)s;
}

QPushButton#playButton {
    background-color: %(TEXT)s;
    border: none;
    border-radius: 18px;
    padding: 6px;
}

QPushButton#playButton:hover {
    background-color: %(GREEN_HOVER)s;
    transform: scale(1.04);
}

QPushButton#folderButton {
    background-color: %(GREEN)s;
    color: %(BG)s;
    border: none;
    border-radius: 20px;
    padding: 12px 24px;
    font-weight: bold;
    font-size: 14px;
}

QPushButton#folderButton:hover {
    background-color: %(GREEN_HOVER)s;
}

QSlider::groove:horizontal {
    height: 4px;
    background-color: %(BG_LIGHTER)s;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background-color: %(TEXT)s;
    width: 12px;
    height: 12px;
    margin: -4px 0;
    border-radius: 6px;
}

QSlider::handle:horizontal:hover {
    background-color: %(GREEN)s;
}

QSlider::sub-page:horizontal {
    background-color: %(GREEN)s;
    border-radius: 2px;
}

QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: %(BG_LIGHTER)s;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: transparent;
}
""" % {
    "BG": BG,
    "BG_LIGHT": BG_LIGHT,
    "BG_LIGHTER": BG_LIGHTER,
    "SIDEBAR_BG": SIDEBAR_BG,
    "GREEN": GREEN,
    "GREEN_HOVER": GREEN_HOVER,
    "TEXT": TEXT,
    "TEXT_SECONDARY": TEXT_SECONDARY,
}


def apply_theme(app):
    app.setStyleSheet(SPOTIFY_QSS)
