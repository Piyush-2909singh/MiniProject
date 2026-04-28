import os
from utils.db import execute_db

os.makedirs("database", exist_ok=True)

execute_db("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT,
role TEXT
)
""", commit=True)

print("Database created successfully")