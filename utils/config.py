import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret123')
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    DB_PATH = os.path.join(os.getcwd(), 'database', 'users.db')
    
