from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from bbem.auth import login_required
from bbem.db import get_db

bp = Blueprint('entries', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    entries = db.execute(
        'SELECT e.id, payer_id, payee, date, amount, source, category'
        ' FROM entries e JOIN user u ON e.payer_id = u.id'
        ' ORDER BY date DESC'
    ).fetchall()
    return render_template('entries/index.html', entries=entries)



def init_vars():
    payer = int(request.form['payer_id'])
    payee = request.form['payee']
    date = request.form['date']
    amount = int(float(request.form['amount'])*100)
    source = request.form['source']
    category = request.form['category']
    error = None
    return payer, payee, date, amount, source, category, error


def validate_vars(payee, date, amount, source, category):
    if not payee:
        error = 'Payee is required.'
    elif not date:
        error = 'date is required.'
    elif not amount:
        error = 'Amount is required.'
    elif not source:
        error = 'Source is required.'
    elif not category:
        error = 'Category is required.'
    else:
        error = None
    return error



@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    db = get_db()

    if request.method == 'POST':
        payer, payee, date, amount, source, category, error = init_vars()

        error = validate_vars(payee, date, amount, source, category)

        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO entries (payer_id, payee, date, amount, source, category)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (payer, payee, date, amount, source, category)
            )
            db.commit()
            db.execute(
                'INSERT OR IGNORE INTO category (category)'
                ' VALUES (?)',
                (category,)
            )
            db.commit()
            db.execute(
                'INSERT OR IGNORE INTO source (source)'
                ' VALUES (?)',
                (source,)
            )
            db.commit()
            return redirect(url_for('entries.index'))

    users = db.execute(
        'SELECT id, username FROM user'
    ).fetchall()

    category = db.execute(
        'SELECT category FROM category'
    ).fetchall()

    source = db.execute(
        'SELECT source FROM source'
    ).fetchall()

    return render_template('entries/create.html', users=users, category=category, source=source)


def get_post(id, check_author=True):
    entry = get_db().execute(
        'SELECT e.id, payer_id, payee, date, amount, source, category'
        ' FROM entry e JOIN user u ON p.payer_id = u.id'
        ' WHERE e.id = ?',
            (id,)
    ).fetchone()

    if entry is None:
        abort(404, f"Post id {id} doesn't exist.")
    if check_author and entry['payer_id'] != g.user['id']:
        abort(403)

    return entry


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    entry = get_post(id)

    if request.method == 'POST':
        payer, payee, date, amount, source, category, error = init_vars()

        error = validate_vars(payee, date, amount, source, category)

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE entry SET payer = ?, payee = ?, date = ?, amount = ?, source = ?, category = ?'
                ' WHERE id = ?',
                (payer, payee, date, amount, source, category)
            )
            db.commit()
            return redirect(url_for('entries.index'))
    return render_template('entries/update.html', entry=entry)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM entry WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('entries.index'))
