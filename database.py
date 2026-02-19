import sqlite3

def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table(): 
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXIST users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT         
        )
""")
conn.commit()
conn.close()