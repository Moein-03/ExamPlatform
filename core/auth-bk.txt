# core/auth.py
import sqlite3
import settings
from core import cookie
from datetime import datetime, timedelta

def create_session(user_id):
    session_id = cookie.generate_session_id()
    expires_at = datetime.now() + timedelta(days=7)
    dbc = sqlite3.connect(settings.DB_PATH)
    cursor = dbc.cursor()
    cursor.execute('''
        INSERT INTO sessions (id, user_id, expires_at)
        VALUES (?, ?, ?)
    ''', (session_id, user_id, expires_at.isoformat()))
    dbc.commit()
    dbc.close()
    return session_id

def get_current_user(session_id):
    if not session_id:
        return None
    dbc = sqlite3.connect(settings.DB_PATH)
    dbc.row_factory = sqlite3.Row
    cursor = dbc.cursor()
    cursor.execute('''
        SELECT u.* FROM users u
        JOIN sessions s ON s.user_id = u.id
        WHERE s.id = ? AND s.expires_at > datetime('now') AND u.is_deleted = 0
    ''', (session_id,))
    row = cursor.fetchone()
    dbc.close()
    return dict(row) if row else None

def is_logged_in(session_id):
    return get_current_user(session_id) is not None

def is_admin(user_id):
    if not user_id:
        return False
    dbc = sqlite3.connect(settings.DB_PATH)
    cursor = dbc.cursor()
    cursor.execute('SELECT role FROM users WHERE id = ? AND is_deleted = 0', (user_id,))
    row = cursor.fetchone()
    dbc.close()
    return row is not None and row[0] == 2

def is_teacher(user_id):
    if not user_id:
        return False
    dbc = sqlite3.connect(settings.DB_PATH)
    cursor = dbc.cursor()
    cursor.execute('SELECT role FROM users WHERE id = ? AND is_deleted = 0', (user_id,))
    row = cursor.fetchone()
    dbc.close()
    return row is not None and row[0] >= 1

def is_student(user_id):
    if not user_id:
        return False
    dbc = sqlite3.connect(settings.DB_PATH)
    cursor = dbc.cursor()
    cursor.execute('SELECT role FROM users WHERE id = ? AND is_deleted = 0', (user_id,))
    row = cursor.fetchone()
    dbc.close()
    return row is not None and row[0] == 0

def get_user_role(user_id):
    if not user_id:
        return None
    dbc = sqlite3.connect(settings.DB_PATH)
    cursor = dbc.cursor()
    cursor.execute('SELECT role FROM users WHERE id = ? AND is_deleted = 0', (user_id,))
    row = cursor.fetchone()
    dbc.close()
    return row[0] if row else None

def delete_session(session_id):
    if not session_id:
        return
    dbc = sqlite3.connect(settings.DB_PATH)
    cursor = dbc.cursor()
    cursor.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
    dbc.commit()
    dbc.close()