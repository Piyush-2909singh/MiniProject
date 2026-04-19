import sqlite3
import os

os.makedirs('data', exist_ok=True)

conn = sqlite3.connect('data/app.db')
c = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE ,
    password TEXT ,
    role 
)
""")

conn.commit()
conn.close()

print("Database created and users table initialized.")