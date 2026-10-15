import os
import sys

from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

from Gui.theme import apply_theme
from Gui.sidebar import Sidebar
from Gui.home_page import HomePage
from Gui.now_playing_bar import NowPlayingBar
from core.music_controller import MusicController
from core.database import LibraryDB


def get_music_folder():
    home = os.path.expanduser("~")
    candidates = [
        os.path.join(home, "Music"),
        os.path.join(home, "Music", "Music"),
    ]
    for path in candidates:
        if os.path.isdir(path):
            return path
    return home


def main():
    app = QApplication(sys.argv)
    apply_theme(app)

    controller = MusicController()
    db = LibraryDB()
    music_folder = get_music_folder()

    window = QWidget()
    window.setWindowTitle("Kora")
    window.resize(1100, 650)
    window.setMinimumSize(800, 500)
    window.setWindowIcon(QIcon("images/kora.png"))

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    content = QWidget()
    content_layout = QHBoxLayout()
    content_layout.setContentsMargins(0, 0, 0, 0)
    content_layout.setSpacing(0)

    sidebar = Sidebar()
    home = HomePage()

    content_layout.addWidget(sidebar)
    content_layout.addWidget(home, 1)
    content.setLayout(content_layout)

    bar = NowPlayingBar()

    layout.addWidget(content, 1)
    layout.addWidget(bar)
    window.setLayout(layout)

    def reload_library():
        tracks = db.get_tracks()
        controller.load_tracks(tracks)
        controller.set_volume(bar.volume.value())
        home.set_tracks(tracks)
        return tracks

    def sync_bar():
        track = controller.current_track
        if track:
            bar.set_track_title(controller.track_display_name(track))
            bar.set_playing_state(controller.is_playing())
            home.highlight_current(controller.current_index)

    def remove_track(index):
        tracks = controller.playlist
        if 0 <= index < len(tracks):
            db.hide_track(tracks[index])
            controller.stop()
            reload_library()
            bar.set_playing_state(False)
            bar.set_track_title("No track playing")

    def play_track(index):
        if controller.play(index):
            sync_bar()

    def toggle_play_pause():
        if controller.current_index < 0 and controller.playlist:
            play_track(0)
            return
        controller.toggle_play()
        sync_bar()

    def next_track():
        if controller.next_track():
            sync_bar()

    def prev_track():
        if controller.prev_track():
            sync_bar()

    home.track_selected.connect(play_track)
    home.remove_requested.connect(remove_track)
    bar.play_pause_clicked.connect(toggle_play_pause)
    bar.next_clicked.connect(next_track)
    bar.prev_clicked.connect(prev_track)
    bar.volume_changed.connect(controller.set_volume)

    def poll():
        if controller.has_finished():
            next_track()

    poll_timer = QTimer()
    poll_timer.setInterval(400)
    poll_timer.timeout.connect(poll)
    poll_timer.start()

    found = controller.scan_folder(music_folder)
    db.sync_folder(music_folder, found)
    reload_library()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
