import sqlite3
import hashlib
import os

DB_PATH = "learnova.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            query TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def signup_user(username: str, password: str) -> bool:
    """Create a new user. Returns True on success, False if username exists."""
    if not username or not password:
        return False
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username.strip(), hash_password(password))
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def login_user(username: str, password: str) -> bool:
    """Validate credentials. Returns True if valid."""
    if not username or not password:
        return False
    conn = get_connection()
    cursor = conn.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?",
        (username.strip(), hash_password(password))
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


def save_history(username: str, query: str, response: str) -> None:
    """Save a search query and its response for a user."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO history (username, query, response) VALUES (?, ?, ?)",
        (username, query, response)
    )
    conn.commit()
    conn.close()


def get_history(username: str) -> list[tuple[str, str]]:
    """Get the last 20 searches for a user as list of (query, response) tuples."""
    conn = get_connection()
    cursor = conn.execute(
        "SELECT query, response FROM history WHERE username = ? ORDER BY created_at DESC LIMIT 20",
        (username,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_history(username: str) -> None:
    """Delete all history for a user."""
    conn = get_connection()
    conn.execute("DELETE FROM history WHERE username = ?", (username,))
    conn.commit()
    conn.close()
