import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret123")
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH",
        os.path.join(os.getcwd(), "database", "users.db")
    )
    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER",
        os.path.join(os.getcwd(), "uploads")
    )
    MAX_CONTENT_LENGTH = int(
        os.environ.get("MAX_CONTENT_LENGTH", 5 * 1024 * 1024)
    )

    DB_PATH = DATABASE_PATH
