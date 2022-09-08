"""Flask app for Feedback"""
from sqlite3 import IntegrityError
from flask import Flask, request, redirect, render_template, flash, session
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm, edit_feedback_form
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
        flash("User created!", "success")

        return redirect(f"/users/{new_user.username}")
        
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
            flash("Successfully logged in!", "success")
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Incorrect username or password."]

    return render_template("login.html", form=form)

@app.route("/secret")
def reveal_secrets():
    """Reveal secrets only to users who are logged in."""
    if "username" not in session:
        flash("Please log in to view this page.", "warning")
        return redirect("/login")

    return render_template("secret.html")

@app.route("/users/<username>")
def show_user(username):
    if "username" not in session:
        flash("Please log in to view this page.", "warning")
        return redirect("/login")

    user = User.query.get_or_404(username)
    feedback = user.user_feedback
    
    return render_template("show_user.html", user=user, feedback=feedback)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    if "username" not in session:
        flash("Please log in to view this page.", "warning")
        return redirect("/login")

    user = User.query.get_or_404(username)

    if session["username"] != user.username:
        flash("You are not authorized to view this page.", "warning")
        redirect("/login")
    
    db.session.delete(user)
    db.session.commit()
    flash("User deleted.", "danger")
    return redirect("/register")

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    if "username" not in session:
        flash("Please log in to view this page.", "warning")
        return redirect("/login")

    user = User.query.get_or_404(username)
    form = FeedbackForm()

    if session["username"] != user.username:
        flash("You are not authorized to view this page.", "warning")
        return redirect(f"/users/{session['username']}")
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        
        flash("Feedback created!", "success")

        return redirect(f"/users/{username}")
    
    return render_template("add_feedback.html", form=form, user=user)

@app.route("/feedback/<int:id>/update", methods=["GET", "POST"])
def update_feedback(id):
    if "username" not in session:
        flash("Please log in to view this page.", "warning")
        return redirect("/login")

    feedback = Feedback.query.get_or_404(id)
    form = edit_feedback_form(feedback)

    if session["username"] != feedback.username:
        flash("You are not authorized to view this page.", "warning")
        return redirect(f"/users/{session['username']}")

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback.title = title
        feedback.content = content

        db.session.add(feedback)
        db.session.commit()

        flash("Feedback updated.", "success")
        return redirect(f"/users/{feedback.username}")

    return render_template("edit_feedback.html", form=form)

@app.route("/logout")
def logout_user():
    """Log out user and redirect to login page."""

    session.pop("username")

    return redirect("/login")


