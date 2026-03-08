from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os
from rag import read_pdf


app = Flask(__name__)


app.config["SECRET_KEY"] = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

UPLOAD_FOLDER="uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db=SQLAlchemy(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

pdf_text=""

class User(UserMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(150),nullable=False)
    password=db.Column(db.String(150),nullable=False)


@app.route('/')     # yahan se redirect kr dega to login page
def start():
    return redirect("/login")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        user= User.query.filter_by(username=username,password=password).first()

        if user:
            login_user(user)
            return redirect("/home")

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

    file=os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

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

