from wtforms import BooleanField, StringField, PasswordField, SubmitField, validators, Label
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
