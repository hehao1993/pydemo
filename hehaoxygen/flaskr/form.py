from wtforms import BooleanField, StringField, PasswordField, SubmitField, validators, TextAreaField
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    submit = SubmitField('Sign In')


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [validators.DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')


class ThreeForm(FlaskForm):
    title = StringField('Title', [validators.Length(min=2, max=25)])
    script = TextAreaField('Script', [validators.DataRequired()])
    submit = SubmitField('Submit')
