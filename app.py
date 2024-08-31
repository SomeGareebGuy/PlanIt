from flask import Flask, request, redirect, session, url_for, render_template
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__) 

app.config["SESSION_TYPE"] = "filesystem"

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
