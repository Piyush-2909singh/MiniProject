from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os
from rag import read_pdf


app = Flask(__name__)



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




