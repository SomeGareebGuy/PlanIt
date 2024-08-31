from flask import Flask, request, redirect, session, url_for, render_template
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

app.config["SESSION_TYPE"] = "filesystem"

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True, nullable=False)
    hash_id = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"Name : {self.first_name}, Age: {self.age}"

Session(app)

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("email"):
            error = "Must provide email/username."
            return render_template("login.html", error=error)

        elif not request.form.get("password"):
            error = "Must provide password."
            return render_template("login.html", error=error)

        user = Profile.query.filter((Profile.email == request.form.get("email")) | (
            Profile.username == request.form.get("email"))).first()

        if not user or not check_password_hash(user.hash_id, request.form.get("password")):
            error = "Incorrect username/password."
            return render_template("login.html", error=error)
        
        session["user_id"] = user.id

        return redirect("/")

    else:
        return render_template("login.html")

