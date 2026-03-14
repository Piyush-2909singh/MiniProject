from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os
import sqlite3


app = Flask(__name__)
app.secret_key = "secret123"


login_manager=LoginManager()
login_manager.init_app(app)


os.makedirs("uploads", exist_ok=True)


def init_db():
    conn=sqlite3.connect("users.db")
    c=conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


    init_db()

class User(UserMixin):

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password





@login_manager.user_loader
def load_user(user_id):

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = c.fetchone()

    conn.close()

    if row:
        return User(row[0], row[1], row[2])

    return None




@app.route('/')     
def start():
    if current_user.is_authenticated:
        return render_template("home.html", username=current_user.username)

    return render_template("home.html", username=None)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
        )

        row = c.fetchone()
        conn.close()

        if row:
            user = User(row[0], row[1], row[2])
            login_user(user)
            return redirect("/")

    return render_template("login.html")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username,password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")



@app.route('/home')
@login_required
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    file = request.files["file"]

    if file:
        file.save("uploads/" + file.filename)

    return redirect("/admin")



@app.route("/admin")
@login_required
def admin():

    return render_template("admin.html")


@app.route("/ask", methods=["POST"])
@login_required
def ask():
    data = request.get_json()

    query = data["query"]

    answer, sources = generate_answer(query)

    return jsonify({
        "answer": answer,
        "sources": sources
    })




@app.route("/logout")
@login_required
def logout():

    logout_user()
    return redirect("/")


@app.route("/chat")
@login_required
def chat():

    return render_template("chat.html")


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)

