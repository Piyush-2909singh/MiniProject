import sqlite3

from config import Config


def execute_db(query, params=(), fetchone=False, fetchall=False, commit=False, raise_on_error=False):
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        cur = conn.cursor()
        cur.execute(query, params)
        result = None
        if fetchone:
            result = cur.fetchone()
        elif fetchall:
            result = cur.fetchall()
        if commit:
            conn.commit()
        conn.close()
        return result
    except Exception as e:
        print("DB Error:", e)
        if raise_on_error:
            raise
        return None
