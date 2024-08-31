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

        rows = db.execute(
            "SELECT * FROM users WHERE email = ? OR username = ?", request.form.get(
                "email"), request.form.get("email")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            error = "Incorrect username/password."
            return render_template("login.html", error=error)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")
@app.route('/register', methods=["POST", "GET"])
def register():
    session.clear()

    if request.method == "POST":
        if not request.form.get("email"):
            error="Must provide email"
            return render_template('register.html', error=error)

        elif not request.form.get("password"):
            error="Must provide password"
            return render_template('register.html', error=error)

        elif not request.form.get("username"):
            error = "Must provide username"
            return render_template('register.html', error=error)

        elif request.form.get("password") != request.form.get("confirmation"):
            error="Password must be same as confirm password"
            return render_template('register.html', error=error)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        if len(rows) != 0:
            error = "Username already exists."
            return render_template('register.html', error=error)

        rows = db.execute(
            "SELECT * FROM users WHERE email = ?", request.form.get(
                "email")
        )

        if len(rows) != 0:
            error="Account with the given email already exists"
            return render_template('register.html', error=error)

        db.execute(
            "INSERT INTO users (email, hash, username) VALUES (?, ?, ?)",
            request.form.get("email"),
            generate_password_hash(request.form.get("password")),
            request.form.get("username")
        )

        return redirect("/")

    else:
        return render_template('register.html')



