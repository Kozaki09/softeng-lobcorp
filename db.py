"""Database initialization and helper functions"""
import sqlite3
from werkzeug.security import generate_password_hash


def get_db(database="app.db"):
    """Get database connection"""
    db = sqlite3.connect(database)
    db.row_factory = sqlite3.Row
    return db


def init_db(database="app.db"):
    """Initialize database and create tables"""
    db = get_db(database)
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Check if admin user exists, if not create it
    user = db.execute("SELECT * FROM users WHERE username = ?", ("admin",)).fetchone()
    if not user:
        password_hash = generate_password_hash("password")
        db.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
            ("admin", password_hash, "admin@example.com")
        )

    db.commit()
    db.close()


def get_user_by_username(username, database="app.db"):
    """Get user from database by username"""
    db = get_db(database)
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    db.close()
    return user


def create_user(username, password_hash, email=None, database="app.db"):
    """Create a new user in the database"""
    db = get_db(database)
    try:
        db.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
            (username, password_hash, email)
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        db.close()
