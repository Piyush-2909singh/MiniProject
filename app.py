from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user



app = Flask(__name__)



@app.route('/')
def home():
    return redirect("/login")


@app.route('/login')
def login():
    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        user=User.query.filter_by(username=username,password=password).first()

        if user:
            login_user(user)
            return redirect("/home")

    return render_template("login.html")



