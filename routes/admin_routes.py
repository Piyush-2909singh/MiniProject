import logging
import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from markupsafe import escape

from ingestion import ingest_document
from utils.auth import role_required
from config import Config
from utils.validators import (
    allowed_file_extension,
    allowed_mime_type,
    sanitize_filename,
    validate_file_size,
    validate_text,
)

admin_bp = Blueprint('admin', __name__)
logger = logging.getLogger(__name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def admin():
    if request.method == 'POST':
        try:
            max_size = current_app.config.get('MAX_CONTENT_LENGTH', 5 * 1024 * 1024)
            if not validate_file_size(request.content_length, max_size):
                flash('File is too large. Max size is 5MB.', 'error')
                return render_template('admin.html'), 400

            file = request.files.get('file')
            if not file or not allowed_file_extension(file.filename):
                flash('Please upload a valid PDF file.', 'error')
                return render_template('admin.html'), 400
            if not allowed_mime_type(file.mimetype):
                flash('Invalid file type.', 'error')
                return render_template('admin.html'), 400

            raw_category = request.form.get('category', '')
            category = str(escape(raw_category)).strip() or 'general'
            if raw_category and not validate_text(category, max_len=50):
                flash('Invalid category.', 'error')
                return render_template('admin.html'), 400

            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            filename = sanitize_filename(file.filename)
            if not filename:
                flash('Invalid filename.', 'error')
                return render_template('admin.html'), 400
            save_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(save_path)
            success = ingest_document(
                save_path,
                uploaded_by=getattr(current_user, 'username', 'unknown'),
                category=category
            )
            if not success:
                flash('An error occurred during file processing.', 'error')
                return render_template('admin.html'), 500
            from search import reload_index
            reload_index()
            flash('File uploaded and indexed successfully!', 'success')
        except Exception as e:
            logger.error(f"File upload failed: {e}")
            flash('An error occurred during file upload.', 'error')
    return render_template('admin.html')
