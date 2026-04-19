import sqlite3
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self,id,username,role):

        self.id=id
        self.username=username
        self.role=role


def get_user(user_id):

    conn=sqlite3.connect("database/users.db")
    cur=conn.cursor()

    cur.execute(
    "SELECT id,username,role FROM users WHERE id=?",
    (user_id,)
    )

    row=cur.fetchone()

    conn.close()

    if row:
        return User(row[0],row[1],row[2])

    return None