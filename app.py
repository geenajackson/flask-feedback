"""Flask app for Feedback"""
from sqlite3 import IntegrityError
from flask import Flask, jsonify, request, redirect, render_template, flash, session
from models import db, connect_db, User
from forms import RegisterUserForm, LoginUserForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def redirect_to_register():
    """Redirects the User to /register"""
    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Shows form for registering user"""
    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors = ["Username or email taken. Please try again."]
            return render_template("register.html", form=form)

        session["username"] = new_user.username

        return redirect("/secret")
        
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login_user():
    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        #authenticate method returns a user or False
        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect("/secret")

        else:
            form.username.errors = ["Incorrect username or password."]

    return render_template("login.html", form=form)

@app.route("/secret")
def reveal_secrets():
    return render_template("secret.html")