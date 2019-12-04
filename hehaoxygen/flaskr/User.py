from flask_login import UserMixin

from flaskr.db import get_db


class User(UserMixin):
    pass


def get_user_by_id(user_id):
    return get_db().execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()


def get_user_by_name(username):
    return get_db().execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()
