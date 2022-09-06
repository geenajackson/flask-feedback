"""Flask app for Feedback"""
from flask import Flask, jsonify, request, redirect, render_template, flash
from models import db, connect_db
from forms import RegisterUserForm

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
def show_register():
    """Shows form for registering user"""
    form = RegisterUserForm()
    return render_template("register.html", form=form)