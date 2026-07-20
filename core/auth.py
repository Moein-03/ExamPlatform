# core/auth.py
import sqlite3
import settings
import time

_sessions = {}
_session_expiry = {}

def create_session(user_id, max_age=604800):
    import uuid
    session_id = str(uuid.uuid4())
    _sessions[session_id] = user_id
    _session_expiry[session_id] = time.time() + max_age
    return session_id

def get_current_user(session_id):
    if not session_id or session_id not in _sessions:
        return None
    if _session_expiry.get(session_id, 0) < time.time():
        delete_session(session_id)
        return None
    return get_user_by_id(_sessions[session_id])

def delete_session(session_id):
    if session_id in _sessions:
        del _sessions[session_id]
    if session_id in _session_expiry:
        del _session_expiry[session_id]

def get_user_by_id(user_id):
    if not settings.DB_PATH.exists():
        return None
    conn = sqlite3.connect(str(settings.DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TBL_users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_role(user_id):
    user = get_user_by_id(user_id)
    return user['role'] if user else None

def is_admin(user_id):
    return get_user_role(user_id) == 'admin'

def is_teacher(user_id):
    return get_user_role(user_id) == 'teacher'

def is_student(user_id):
    return get_user_role(user_id) == 'student'