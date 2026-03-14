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
        username=request.form["username"]
        password=request.form["password"]

        new_user= User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("signup.html")



@app.route('/home')
@login_required
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    global pdf_text

    file=request.files["pdf"]

    path=os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(path)

    pdf_text=read_pdf(path)

    return "PDF uploaded successfully"



@app.route("/ask", methods=["POST"])
@login_required
def ask():
    question=request.form["question"].lower()
    sentences=pdf_text.split(".")

    best_sentence=""
    best_score=0

    for sentence in sentences:
        score=0

        for word in question.split():
            if word in sentence.lower():
                score+=1
        
        if score > best_score:
            best_score=score
            best_sentence=sentence

    if best_sentence:
        return "Answer: " + best_sentence
    
    return "Sorry, I couldn't find an answer."



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)

