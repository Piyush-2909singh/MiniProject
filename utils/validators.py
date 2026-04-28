import re

from werkzeug.utils import secure_filename

USERNAME_PATTERN = re.compile(r'^[A-Za-z0-9_]{3,20}$')
ALLOWED_UPLOAD_EXTENSIONS = {'pdf'}
ALLOWED_UPLOAD_MIMETYPES = {'application/pdf'}


def validate_username(username):
    return bool(username and USERNAME_PATTERN.match(username))


def validate_password(password):
    return bool(password and len(password) >= 6)


def validate_text(text, max_len=500):
    if not text:
        return False
    stripped = str(text).strip()
    return bool(stripped) and len(stripped) <= max_len


def allowed_file_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_UPLOAD_EXTENSIONS


def allowed_mime_type(mimetype):
    return mimetype in ALLOWED_UPLOAD_MIMETYPES


def sanitize_filename(filename):
    return secure_filename(filename or "")


def validate_file_size(content_length, max_size):
    if content_length is None:
        return True
    return content_length <= max_size
