
import logging
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from markupsafe import escape
from services.rag_service import get_answer
from search import has_indexed_documents
from utils.validators import validate_text
import utils.security

chat_bp = Blueprint('chat', __name__)
logger = logging.getLogger(__name__)

@chat_bp.route('/chat')
@login_required
def chat():
    return render_template(
        'chat.html',
        username=current_user.username,
        index_ready=has_indexed_documents()
    )

@chat_bp.route('/chat', methods=['POST'])
@chat_bp.route('/ask', methods=['POST'])
@login_required
@utils.security.limiter.limit("10 per minute")
def ask():
    try:
        data = request.get_json(silent=True) or {}
        logger.info("Chat POST received with keys=%s", list(data.keys()))

        raw_query = data.get('message') or data.get('query') or ''
        query = str(escape(raw_query)).strip()
        if not validate_text(query, max_len=500):
            return jsonify({'error': 'Invalid input.'}), 400

        answer, sources = get_answer(query)
        return jsonify({'answer': answer, 'sources': sources})
    except Exception as e:
        logger.exception("Chat processing failed: %s", e)
        return jsonify({'error': 'An error occurred while processing your request.'}), 500
