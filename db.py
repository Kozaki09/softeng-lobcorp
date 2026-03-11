"""Database initialization and helper functions"""
import sqlite3
from datetime import datetime, timedelta

def get_db(database="app.db"):
    db = sqlite3.connect(database)
    db.row_factory = sqlite3.Row
    return db

def init_db(database="app.db"):
    db = get_db(database)
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS subscription (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            start_date DATETIME NOT NULL,
            end_date DATETIME NOT NULL,
            status TEXT DEFAULT 'active',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    db.commit()
    db.close()

def get_user_by_username(username, database="app.db"):
    db = get_db(database)
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    db.close()
    return user

def get_user_by_id(user_id, database="app.db"):
    db = get_db(database)
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    db.close()
    return user

def create_user(username, password_hash, database="app.db"):
    db = get_db(database)
    try:
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        db.close()

# ── Subscription helpers ──────────────────────────────────────

def get_active_subscription(user_id, database="app.db"):
    """Get active subscription by numeric user_id"""
    db = get_db(database)
    sub = db.execute("""
        SELECT * FROM subscription
        WHERE user_id = ? AND status = 'active' AND end_date > CURRENT_TIMESTAMP
        ORDER BY created_at DESC LIMIT 1
    """, (user_id,)).fetchone()
    db.close()
    return sub

def activate_subscription(user_id, database="app.db"):
    """
    Renew or create a subscription for the user:
    - If an active subscription exists, extend its end_date by 30 days.
    - Otherwise, create a new 30-day active subscription from now.
    """
    db = get_db(database)
    try:
        now = datetime.utcnow()

        existing = db.execute("""
            SELECT id, end_date FROM subscription
            WHERE user_id = ? AND status = 'active'
            ORDER BY created_at DESC LIMIT 1
        """, (user_id,)).fetchone()

        if existing:
            current_end = datetime.fromisoformat(str(existing["end_date"]))
            new_end     = current_end + timedelta(days=30)
            db.execute(
                "UPDATE subscription SET end_date = ? WHERE id = ?",
                (new_end, existing["id"])
            )
        else:
            db.execute("""
                INSERT INTO subscription (user_id, start_date, end_date, status)
                VALUES (?, ?, ?, 'active')
            """, (user_id, now, now + timedelta(days=30)))

        db.commit()
        return True
    finally:
        db.close()

def cancel_subscription(user_id, database="app.db"):
    """Mark the user's active subscription as cancelled."""
    db = get_db(database)
    try:
        cursor = db.execute("""
            UPDATE subscription SET status = 'cancelled'
            WHERE user_id = ? AND status = 'active'
        """, (user_id,))
        db.commit()
        return cursor.rowcount > 0
    finally:
        db.close()