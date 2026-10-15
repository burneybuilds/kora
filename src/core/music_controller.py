import os
import pygame

AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".flac"}


class MusicController:
    def __init__(self):
        pygame.mixer.init()
        self.playlist = []
        self.current_index = -1
        self._playing = False

    def scan_folder(self, folder):
        tracks = []
        for root, _dirs, files in os.walk(folder):
            for name in files:
                if os.path.splitext(name)[1].lower() in AUDIO_EXTENSIONS:
                    tracks.append(os.path.join(root, name))
        tracks.sort(key=str.lower)
        return tracks

    def load_tracks(self, tracks):
        self.stop()
        self.playlist = list(tracks)
        self.current_index = -1

    def play(self, index=None):
        if not self.playlist:
            return False
        if index is not None:
            if not (0 <= index < len(self.playlist)):
                return False
            self.current_index = index
        if self.current_index < 0:
            return False
        try:
            pygame.mixer.music.load(self.playlist[self.current_index])
            pygame.mixer.music.play()
            self._playing = True
            return True
        except pygame.error:
            self._playing = False
            return False

    def pause(self):
        if self._playing:
            pygame.mixer.music.pause()
            self._playing = False

    def resume(self):
        if not self._playing:
            pygame.mixer.music.unpause()
            self._playing = True

    def toggle_play(self):
        if self.is_playing():
            self.pause()
        elif self.current_index >= 0:
            self.resume()
        else:
            self.play(0 if self.playlist else None)

    def stop(self):
        pygame.mixer.music.stop()
        self._playing = False

    def next_track(self):
        if not self.playlist:
            return False
        self.current_index = (self.current_index + 1) % len(self.playlist)
        return self.play()

    def prev_track(self):
        if not self.playlist:
            return False
        if self.current_index <= 0:
            self.current_index = len(self.playlist) - 1
        else:
            self.current_index -= 1
        return self.play()

    def set_volume(self, value):
        pygame.mixer.music.set_volume(max(0.0, min(1.0, value / 100.0)))

    def is_playing(self):
        return self._playing and pygame.mixer.music.get_busy()

    def has_finished(self):
        return self._playing and not pygame.mixer.music.get_busy()

    @property
    def current_track(self):
        if 0 <= self.current_index < len(self.playlist):
            return self.playlist[self.current_index]
        return None

    def track_display_name(self, path):
        return os.path.splitext(os.path.basename(path))[0]
