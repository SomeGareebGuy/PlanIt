from flask import Flask, request, redirect, session, url_for, render_template
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from helpers import login_required

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
        return f"Name : {self.username}, Email: {self.email}"
    

class Itinerary(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    itinerary_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f"User : {self.user_id}, Itinerary: {self.itinerary_id}"
    
class Entry(db.Model):
    entry_id = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.itinerary_id'), nullable=False)
    start_location = db.Column(db.String(20), nullable=False)
    end_location = db.Column(db.String(20), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    mode_of_transport = db.Column(db.String(20), nullable=False)
    next_entry = db.Column(db.Integer, db.ForeignKey('entry.entry_id'), nullable=True)

    def __repr__(self):
        return f"Start : {self.start_location}, End: {self.end_location}, Time: {self.time}, Price: {self.price}, Mode of Transport: {self.mode_of_transport}"
    
class Reviews(db.Model):
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.itinerary_id'),primary_key = True, nullable=False)
    comment = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"Comment : {self.comment}"

class Likes(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('profile.id'), primary_key = True, nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.itinerary_id'), nullable=False)
    like_or_dislike = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"User : {self.user_id}, Itinerary: {self.itinerary_id}, Like/Dislike: {self.like_or_dislike}"


Session(app)

with app.app_context():
    db.create_all()

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

        user = Profile.query.filter_by(
            username=request.form.get("username")).first()

        user = Profile.query.filter_by(
            username=request.form.get("username")).first()


        if user:
            error = "Username already exists."
            return render_template('register.html', error=error)
        
        rows = Profile.query.filter_by(email=request.form.get("email")).all()

        if len(rows) != 0:
            error="Account with the given email already exists"
            return render_template('register.html', error=error)

        new_user = Profile(
            email= request.form.get("email"),
            hash_id = generate_password_hash(request.form.get("password")),
            username = request.form.get("username")
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect("/")

    else:
        return render_template('register.html')

@login_required
@app.route('/profile', methods=["GET", "POST"])
def profile():
    #to see the profile of the person
    return render_template('profile.html')

@app.route('/search', methods=["GET", "POST"])
def search():
    #the search page
    return render_template('search.html')

@app.route('/')
def index():
    #main page
    return render_template('index.html')

@app.route('/create', methods=["GET", "POST"])
def create():
    #for creating iternaries
    return render_template("create.html")

