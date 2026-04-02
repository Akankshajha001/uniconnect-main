"""
Lost & Found Database - SQLite persistent storage
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), 'lost_found.db')


def _get_conn():
    return sqlite3.connect(DB_PATH)


def _init_db():
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS lost_found_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        item_name TEXT,
        category TEXT,
        location TEXT,
        description TEXT,
        reporter_name TEXT,
        reporter_contact TEXT,
        date TEXT,
        status TEXT,
        image_path TEXT,
        verification_data TEXT
    )''')
    # Keep column migration for existing databases
    new_columns = [
        ('secret_details', 'TEXT'),
        ('color', 'TEXT'),
        ('brand', 'TEXT'),
        ('verification_data', 'TEXT'),
        ('pending_claims', 'TEXT')
    ]
    for col_name, col_type in new_columns:
        try:
            c.execute(f'ALTER TABLE lost_found_items ADD COLUMN {col_name} {col_type}')
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()

_init_db()

ITEM_KEYS = ['id', 'type', 'item_name', 'category', 'location', 'description', 'reporter_name', 
             'reporter_contact', 'date', 'status', 'image_path', 'verification_data']

_SELECT_COLS = ', '.join(ITEM_KEYS)


def add_item(item: Dict) -> int:
    """Add a lost or found item to the database. Returns new item id."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''INSERT INTO lost_found_items (
        type, item_name, category, location, description, reporter_name, reporter_contact, 
        date, status, image_path, verification_data
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        item['type'], item['item_name'], item['category'], item['location'], item['description'],
        item['reporter_name'], item['reporter_contact'], item.get('date', datetime.now().strftime('%Y-%m-%d')),
        item.get('status', 'open'), item.get('image_path'), item.get('verification_data')
    ))
    item_id = c.lastrowid
    conn.commit()
    conn.close()
    return item_id


def get_all_items() -> List[Dict]:
    """Get all lost and found items from the database."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute(f'SELECT {_SELECT_COLS} FROM lost_found_items')
    rows = c.fetchall()
    conn.close()
    return [dict(zip(ITEM_KEYS, row)) for row in rows]


def get_item_by_id(item_id: int) -> Optional[Dict]:
    """Get a single item by id."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute(f'SELECT {_SELECT_COLS} FROM lost_found_items WHERE id = ?', (item_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return dict(zip(ITEM_KEYS, row))
    return None


def update_item_status(item_id: int, status: str):
    """Update the status for an item."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('UPDATE lost_found_items SET status = ? WHERE id = ?', (status, item_id))
    conn.commit()
    conn.close()
