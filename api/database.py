import datetime
import sqlite3

from models import Note, User


def get_db():
    """ connects to the sqlite db"""
    db = sqlite3.connect('notes_app.db')
    db.row_factory = sqlite3.Row
    return db

def close_db(db):
    db.close()

def create_tables():
    db = get_db()
    cursor = db.cursor()

    user_sql = """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )  
            """
    
    cursor.execute(user_sql)

    notes_sql = """
            
                CREATE TABLE IF NOT EXISTS notes (
                    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    modified_at TEXT NOT NULL
                )
            """
    
    cursor.execute(notes_sql)

    close_db(db)

def add_user(username, password, email) -> User:
    db = get_db()
    cursor = db.cursor()

    add_user_sql = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
    cursor.execute(add_user_sql, (username, password, email))
    db.commit()
    close_db(db)

    return get_user_by_username(username)

def get_user_by_username(username):
    db = get_db()
    cursor = db.cursor()

    get_user_sql = "SELECT * FROM users WHERE users.username = ?"
    cursor.execute(get_user_sql, (username,))

    user = cursor.fetchone()
    close_db(db)

    return user

def add_note(user_id, content):
    db = get_db()
    cursor = db.cursor()

    add_note_sql = "INSER INTO notes (content, user_id, created_at, modified_at)"
    created_at = datetime.datetime.now()
    modified_at = created_at

    cursor.execute(add_note_sql, (content, user_id, created_at, modified_at))
    db.commit()
    close_db(db)

def get_notes_by_user(user_id):
    db = get_db()
    cursor = db.cursor()

    get_notes_sql = "SELECT * FROM notes WHERE notes.user_id = ?"
    cursor.execute(get_notes_sql, (user_id,))

    close_db(db)

    return cursor.fetchall()

def get_note_by_id(note_id, user_id):
    db = get_db()
    cursor = db.cursor()

    get_note_sql = "SELECT * FROM notes WHERE notes.note_id = ? AND notes.user_id = ?"
    cursor.execute(get_note_sql, (note_id, user_id))

    result = cursor.fetchone()

    close_db(db)

    if result: 
        return Note(**result)
    return None

def update_note(note_id, user_id, content):
    db = get_db()
    cursor = db.cursor()

    update_note_sql = "UPDATE notes SET content = ? WHERE user_id = ? and note_id = ?"
    cursor.execute(update_note_sql, (content, user_id, note_id))

    db.commit()
    close_db(db)
    if cursor.rowcount > 0:
        return get_note_by_id(user_id, note_id)
    else: 
        return None
