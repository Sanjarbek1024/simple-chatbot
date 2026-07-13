import sqlite3
from datetime import datetime
import uuid

database_name = 'chat.db'

def get_connection():
    return sqlite3.connect(database_name)

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            message TEXT,
            created_at TEXT
        )                   
    """)
    
    connection.commit()
    connection.close()
    
def get_last_session():
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT session_id
        FROM messages
        ORDER BY id DESC
        LIMIT 1
    """)
    
    row = cursor.fetchone()
    
    connection.close
    
    if row:
        return row[0]

    return str(uuid.uuid4())

def save_message(session_id, role, message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages(session_id,role,message,created_at)
        VALUES(?,?,?,?)
    """, (
        session_id,
        role,
        message,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()
    
def load_history(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role,message
        FROM messages
        WHERE session_id=?
        ORDER BY id
    """, (session_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows