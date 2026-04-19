import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import os
from pypdf import PdfReader
from utils.config import Config
from vector_store import add_document

admin_bp = Blueprint('admin', __name__)
logger = logging.getLogger(__name__)


def _index_pdf(file_path):

    chunk_size = 500
    reader = PdfReader(file_path)
    text = ""


    for page in reader.pages:

        page_text = page.extract_text() or ""
        text += page_text


    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        if chunk.strip():
            add_document(chunk, file_path)

@admin_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if getattr(current_user, 'role', None) != 'admin':
        flash('Admin access only.', 'error')
        return redirect(url_for('home'))
    

    if request.method == 'POST':
        try:

            file = request.files.get('file')

            if not file or not file.filename.lower().endswith('.pdf'):
                flash('Please upload a valid PDF file.', 'error')
                return redirect(url_for('admin.admin'))
            
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            save_path = os.path.join(Config.UPLOAD_FOLDER, file.filename)

            file.save(save_path)

            _index_pdf(save_path)
            flash('File uploaded and indexed successfully!', 'success')


        except Exception as e:

            logger.error(f"File upload failed: {e}")
            flash('An error occurred during file upload.', 'error')

            
    return render_template('admin.html')
