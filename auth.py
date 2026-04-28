from flask_login import UserMixin
from utils.db import execute_db

class User(UserMixin):

    def __init__(self,id,username,role):

        self.id=id
        self.username=username
        self.role=role


def get_user(user_id):
    row = execute_db(
        "SELECT id,username,role FROM users WHERE id=?",
        (user_id,),
        fetchone=True
    )

    if row:
        return User(row[0], row[1], row[2])

    return None