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




