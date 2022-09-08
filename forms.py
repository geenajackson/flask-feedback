from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class RegisterUserForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email Address", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginUserForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Form for adding feedback."""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = TextAreaField("Content", validators=[InputRequired()])

#this function is created to allow default values to come from the feedback parameter
def edit_feedback_form(feedback):
    """Function for editing feedback"""
    class EditFeedbackForm(FlaskForm):
        """Form for editing feedback."""
        title = StringField("Title", default=feedback.title, validators=[InputRequired(), Length(max=100)])
        content = TextAreaField("Content", default=feedback.content, validators=[InputRequired()])
    
    return EditFeedbackForm()