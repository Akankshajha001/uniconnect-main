"""
User Database - SQLite persistent user management with signup/login
Industry-standard security with bcrypt password hashing
"""

import sqlite3
from typing import Dict, Optional
import os

try:
    import bcrypt
    USE_BCRYPT = True
except ImportError:
    import hashlib 
    USE_BCRYPT = False

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')


def _get_conn():
    return sqlite3.connect(DB_PATH)


def _init_db():
    conn = _get_conn()
    c = conn.cursor()
    
    try:
        c.execute("SELECT id, name, email, password_hash FROM users LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("DROP TABLE IF EXISTS user_activity")
        c.execute("DROP TABLE IF EXISTS users")
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        last_login TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_activity (
        user_id INTEGER PRIMARY KEY,
        items_reported INTEGER DEFAULT 0,
        notes_uploaded INTEGER DEFAULT 0,
        notes_downloaded INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    try:
        c.execute('ALTER TABLE users ADD COLUMN created_at TEXT DEFAULT CURRENT_TIMESTAMP')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE users ADD COLUMN last_login TEXT')
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

_init_db()


def hash_password(password: str) -> str:
    """Hash password using bcrypt (industry standard) or SHA256 fallback"""
    if USE_BCRYPT:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    else:
        import hashlib
        return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    if USE_BCRYPT:
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except ValueError:
            import hashlib
            return hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed
    else:
        import hashlib
        return hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed


def signup_user(name: str, email: str, password: str) -> bool:
    """Register a new user. Returns True if successful, False if user/email exists."""
    email = email.strip().lower()

    conn = _get_conn()
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO users (name, roll_no, email, password_hash) VALUES (?, ?, ?, ?)''',
                  (name, email, hash_password(password)))
        user_id = c.lastrowid
        c.execute('''INSERT INTO user_activity (user_id) VALUES (?)''', (user_id,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
def login_user(email: str, password: str) -> Optional[Dict]:
    """Authenticate user by email and password. Returns user dict if valid, else None."""
    email = email.strip().lower()

    conn = _get_conn()
    c = conn.cursor()

    c.execute(
        '''SELECT id, name, email, password_hash
           FROM users
           WHERE LOWER(email) = LOWER(?)''',
        (email,)
    )

    row = c.fetchone()

    if row and verify_password(password, row[3]):
        c.execute(
            'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?',
            (row[0],)
        )

        conn.commit()
        conn.close()

        return {
            'id': row[0],
            'name': row[1],
            'email': row[2]
        }

    conn.close()
    return None


def update_user_activity(user_id: int, activity_type: str):
    """Update user activity count in DB. Only tracks notes_downloaded cumulatively."""
    if not user_id or not isinstance(user_id, (int, float)):
        return

    user_id = int(user_id)

    conn = _get_conn()
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO user_activity (user_id) VALUES (?)', (user_id,))

    if activity_type == 'note_downloaded':
        c.execute('UPDATE user_activity SET notes_downloaded = notes_downloaded + 1 WHERE user_id = ?', (user_id,))

    conn.commit()
    conn.close()
