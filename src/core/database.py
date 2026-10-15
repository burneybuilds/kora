import os
import sqlite3

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "kora.db",
)


class LibraryDB:
    def __init__(self, path=DB_PATH):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_tables()

    def _create_tables(self):
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS folders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE NOT NULL
            );
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                folder_id INTEGER,
                hidden INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (folder_id) REFERENCES folders(id) ON DELETE CASCADE
            );
            """
        )
        self.conn.commit()
        self._migrate()

    def _migrate(self):
        cols = [r[1] for r in self.conn.execute("PRAGMA table_info(tracks)").fetchall()]
        if "hidden" not in cols:
            self.conn.execute(
                "ALTER TABLE tracks ADD COLUMN hidden INTEGER NOT NULL DEFAULT 0"
            )
            self.conn.commit()

    def add_folder(self, path):
        self.conn.execute("INSERT OR IGNORE INTO folders (path) VALUES (?)", (path,))
        self.conn.commit()
        row = self.conn.execute("SELECT id FROM folders WHERE path = ?", (path,)).fetchone()
        return row[0]

    def get_folders(self):
        return [r[0] for r in self.conn.execute("SELECT path FROM folders ORDER BY path")]

    def get_tracks(self):
        rows = self.conn.execute(
            "SELECT path FROM tracks WHERE hidden = 0 ORDER BY title COLLATE NOCASE"
        ).fetchall()
        return [r[0] for r in rows]

    def hide_track(self, path):
        self.conn.execute("UPDATE tracks SET hidden = 1 WHERE path = ?", (path,))
        self.conn.commit()

    def sync_folder(self, folder_path, found_paths):
        folder_id = self.add_folder(folder_path)
        known = {
            r[0]
            for r in self.conn.execute(
                "SELECT path FROM tracks WHERE folder_id = ?", (folder_id,)
            )
        }
        found = set(found_paths)
        to_add = found - known
        if to_add:
            self.conn.executemany(
                "INSERT OR IGNORE INTO tracks (path, title, folder_id, hidden) VALUES (?, ?, ?, 0)",
                [
                    (p, os.path.splitext(os.path.basename(p))[0], folder_id)
                    for p in to_add
                ],
            )
        gone = known - found
        if gone:
            self.conn.executemany(
                "DELETE FROM tracks WHERE path = ?",
                [(p,) for p in gone],
        )
        self.conn.commit()
        self._migrate()

    def _migrate(self):
        cols = [
            r[1]
            for r in self.conn.execute("PRAGMA table_info(tracks)").fetchall()
        ]
        if "hidden" not in cols:
            self.conn.execute(
                "ALTER TABLE tracks ADD COLUMN hidden INTEGER NOT NULL DEFAULT 0"
            )
            self.conn.commit()

    def close(self):
        self.conn.close()
