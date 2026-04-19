import sqlite3
from flask_login import UserMixin
from utils.config import Config
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt()

class User(UserMixin):

    def __init__(self, id, username, password, role='user'):
        self.id = id

        self.username = username
        self.password = password
        self.role = role or 'user'

def validate_username(username):
    return bool(username and re.match(r'^[A-Za-z0-9_]{3,32}$', username))


def validate_password(password):
    return bool(password and len(password) >= 6)


def authenticate_user(username, password):


    if not validate_username(username) or not validate_password(password):
        return None
    
    conn = sqlite3.connect(Config.DB_PATH)
    c = conn.cursor()


    c.execute("SELECT * FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()


    if row and bcrypt.check_password_hash(row[2], password):
        return User(row[0], row[1], row[2], row[3] if len(row) > 3 else 'user')
    return None





def authenticate_user(username, password):


    if not validate_username(username) or not validate_password(password):
        return None
    
    conn = sqlite3.connect(Config.DB_PATH)
    c = conn.cursor()


    c.execute("SELECT * FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()


    if row and bcrypt.check_password_hash(row[2], password):
        return User(row[0], row[1], row[2], row[3] if len(row) > 3 else 'user')
    return None




def register_user(username, password):

    if not validate_username(username):
        return False, "Invalid username. Use 3-32 letters, numbers, or underscores."
    if not validate_password(password):

        return False, "Password must be at least 6 characters."
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    
    try:

        conn = sqlite3.connect(Config.DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users(username, password, role) VALUES (?, ?, ?)", (username, pw_hash, 'user'))
        conn.commit()
        conn.close()
        return True, "Registered successfully"
    
    
    except sqlite3.IntegrityError:
        return False, "Username already exists"
