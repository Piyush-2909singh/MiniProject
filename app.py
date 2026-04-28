
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from flask_login import LoginManager, current_user
from flask_cors import CORS

from config import Config

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # --- Security ---
    from utils.security import init_security
    csrf, limiter = init_security(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # User loader import moved to auth_service
    from services.auth_service import User
    from utils.db import execute_db
    @login_manager.user_loader
    def load_user(user_id):
        row = execute_db("SELECT * FROM users WHERE id=?", (user_id,), fetchone=True)
        if row:
            return User(row[0], row[1], row[2], row[3] if len(row) > 3 else 'user')
        return None

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.chat_routes import chat_bp
    from routes.admin_routes import admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def home():
        if current_user.is_authenticated:
            return render_template("home.html", username=current_user.username)
        return render_template("home.html", username=None)

    def wants_json():
        return request.is_json or request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']

    @app.errorhandler(400)
    def bad_request(_error):
        message = 'Bad request.'
        if wants_json():
            return jsonify({'error': message}), 400
        return message, 400

    @app.errorhandler(404)
    def not_found(_error):
        message = 'Resource not found.'
        if wants_json():
            return jsonify({'error': message}), 404
        return message, 404

    @app.errorhandler(500)
    def server_error(_error):
        message = 'An internal error occurred.'
        if wants_json():
            return jsonify({'error': message}), 500
        return message, 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
