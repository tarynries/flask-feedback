from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=20)],)
    password = PasswordField("Password", validators=[InputRequired()],)
    email = StringField("Email", validators=[InputRequired(), Length(max=50)],)
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)],)
    last_name = StringField("Last Name", validators=[InputRequired(),Length(max=30)],)

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=20)],)
    password = PasswordField("Password", validators=[InputRequired()],)

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=20)],)
    content = TextAreaField("Content", validators=[InputRequired(), Length(max=150)],)
    username = StringField("Username", validators=[InputRequired(), Length(max=20)],)

class DeleteForm(FlaskForm):
    """Blank"""