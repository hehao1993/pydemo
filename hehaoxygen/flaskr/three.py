from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from flask_login import current_user
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.form import ThreeForm

bp = Blueprint('three', __name__)


@bp.route('/')
def index():
    db = get_db()
    threes = db.execute(
        'SELECT p.id, title, script, created, author_id, username'
        ' FROM three p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('three/index.html', threes=threes)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = ThreeForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        script = form.script.data

        db = get_db()
        db.execute(
            'INSERT INTO three (title, script, author_id) VALUES (?, ?, ?)',
            (title, script, current_user.id)
        )
        db.commit()
        return redirect(url_for('three.index'))

    return render_template('three/create.html', form=form)


def get_three(id, check_author=True):
    three = get_db().execute(
        'SELECT p.id, title, script, created, author_id, username'
        ' FROM three p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if three is None:
        abort(404, "Three id {0} doesn't exist.".format(id))

    if check_author and three['author_id'] != current_user.id:
        abort(403)

    return three


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    form = ThreeForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        script = form.script.data

        db = get_db()
        db.execute(
            'UPDATE three SET title = ?, script = ? WHERE id = ?',
            (title, script, id)
        )
        db.commit()
        return redirect(url_for('three.index'))

    three = get_three(id)
    form.title.data = three['title']
    form.script.data = three['script']
    return render_template('three/update.html', three=three, form=form)


@bp.route('/<int:id>/delete')
@login_required
def delete(id):
    get_three(id)
    db = get_db()
    db.execute('DELETE FROM three WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('three.index'))


@bp.route('/<int:id>/detail')
def detail(id):
    three = get_three(id, check_author=False)

    return render_template('three/detail.html', three=three)
