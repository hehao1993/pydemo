import functools
import flask_login
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from flask_login import current_user
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.User import get_user_by_name, User
from flaskr.db import get_db
from flaskr.form import RegistrationForm, LoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif get_user_by_name(username) is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error, 'danger')

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        error = None
        user = get_user_by_name(username)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            fl_user = User()
            fl_user.id = user['id']
            flask_login.login_user(fl_user)
            return redirect(url_for('index'))

        flash(error, 'danger')

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
