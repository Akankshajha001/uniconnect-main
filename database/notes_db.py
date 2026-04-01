"""
Notes Exchange Database - SQLite persistent storage
"""

import sqlite3
import os
from datetime import datetime
from typing import Dict, List

DB_PATH = os.path.join(os.path.dirname(__file__), 'notes.db')


def _get_conn():
    return sqlite3.connect(DB_PATH)


def _init_db():
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        topic TEXT,
        semester TEXT,
        uploaded_by TEXT,
        file_name TEXT,
        file_path TEXT,
        description TEXT,
        upload_date TEXT,
        downloads INTEGER DEFAULT 0,
        rating REAL DEFAULT 0.0
    )''')
    try:
        c.execute('ALTER TABLE notes ADD COLUMN file_path TEXT')
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

_init_db()

NOTE_KEYS = ['id', 'subject', 'topic', 'semester', 'uploaded_by', 'file_name', 
             'file_path', 'description', 'upload_date', 'downloads', 'rating']


def add_note(note: Dict) -> int:
    """Add a note to the database. Returns new note id."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''INSERT INTO notes (
        subject, topic, semester, uploaded_by, file_name, file_path, description, upload_date, downloads, rating
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        note['subject'], note['topic'], note['semester'], note['uploaded_by'], note['file_name'],
        note.get('file_path', ''), note['description'], 
        note.get('upload_date', datetime.now().strftime('%Y-%m-%d')),
        note.get('downloads', 0), note.get('rating', 0.0)
    ))
    note_id = c.lastrowid
    conn.commit()
    conn.close()
    return note_id


def get_all_notes() -> List[Dict]:
    """Get all notes from the database."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute(f'SELECT {", ".join(NOTE_KEYS)} FROM notes')
    rows = c.fetchall()
    conn.close()
    return [dict(zip(NOTE_KEYS, row)) for row in rows]


def get_notes_by_subject(subject: str) -> List[Dict]:
    """Get all notes for a given subject."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute(f'SELECT {", ".join(NOTE_KEYS)} FROM notes WHERE subject = ?', (subject,))
    rows = c.fetchall()
    conn.close()
    return [dict(zip(NOTE_KEYS, row)) for row in rows]


def increment_download(note_id: int):
    """Increment the download count for a note."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('UPDATE notes SET downloads = downloads + 1 WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()
