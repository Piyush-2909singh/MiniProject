from flask import Flask, render_template
from flask_login import LoginManager, current_user
from utils.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    from utils.security import init_security
    csrf, limiter = init_security(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    
    from services.auth_service import User
    @login_manager.user_loader
    def load_user(user_id):
        import sqlite3
        conn = sqlite3.connect(Config.DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id=?", (user_id,))
        row = c.fetchone()
        conn.close()
        if row:
            return User(row[0], row[1], row[2], row[3] if len(row) > 3 else 'user')
        return None

    
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

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

