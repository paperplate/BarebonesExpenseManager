import csv
from datetime import datetime
import functools
import json
import os
from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for
)

import flask_csv

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from bbem.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

ALLOWED_EXTENSIONS = ['csv']

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO user (username, password) VALUES (?, ?)',
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f'User {username} is already registered.'
            else:
                return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/admin', methods=('GET', 'POST'))
@login_required
def admin():
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM user'
    ).fetchall()

    category = db.execute(
            'SELECT * FROM category'
    ).fetchall()

    source = db.execute(
            'SELECT * FROM source'
    ).fetchall()

    flash(error)
    return render_template('auth/admin.html', user=user, category=category, source=source)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('auth.import_data', filename=filename))
    return render_template('auth/upload.html')


@bp.route('/import_data', methods=('GET', 'POST'))
@login_required
def import_data():
    if request.method == 'POST':
        db = get_db()
        rows = []
        for k,v in request.form.lists():
            kl = k.lower()
            if 'date' in kl:
                rows += [v]
            elif 'description' in kl:
                rows += [v]
            elif 'category' in kl:
                rows += [v]
            elif 'cost' in kl:
                rows += [v]
            elif 'sean' in kl:
                rows += [v]
            elif 'weixi' in kl:
                rows += [v]

        users = [ u['id']  for u in db.execute(
            'SELECT id, username FROM user'
        ).fetchall()]

        payer = [users[int(float(r[0]) - float(r[1]) > 0)] for r in zip(*rows[-2:])]

        categories = [c[1:-1] for c in rows[2]]
        sources = ['empty']*len(payer)

        tbl = zip(*([payer] + 
            [[datetime.fromisoformat(d[1:-1]) for d in rows[0]]] +
            [[p[1:-1].strip() for p in rows[1]]] +
            [categories] +
            [[int(float(a[1:-1])*100.0) for a in rows[3]]] + 
            [sources]))

        db.executemany(
            'INSERT OR IGNORE INTO category (category)'
            ' VALUES (?)',
            (((c,) for c in categories))
        )
        db.commit()
        db.executemany(
            'INSERT OR IGNORE INTO source (source)'
            ' VALUES (?)',
            (((s,) for s in sources))
        )
        db.commit()
        db.executemany(
            'INSERT INTO entries (payer_id, date, payee, category, amount, source)'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            (tbl)
        )
        db.commit()
        return redirect(url_for('index'))

    with open(os.path.join(current_app.config['UPLOAD_FOLDER'], request.args.get('filename')), newline='') as f:
        contents = list(csv.reader(f, delimiter=',', quotechar='|'))

    return render_template('auth/import_data.html', headers=contents[0], dat=contents[1:])


# https://stackoverflow.com/questions/3286525/return-sql-table-as-json-in-python
def query2json(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    return (r[0] if r else None) if one else r


@bp.route('/report', methods=('GET',))
@login_required
def report():
    db = get_db()
    error = None
    user = query2json('SELECT id, username FROM user')
    category = query2json('SELECT * FROM category')
    source = query2json('SELECT * FROM source')
    entries = query2json(
        'SELECT e.id, u.username, payer_id, payee, date, amount, source, category'
        ' FROM entries e JOIN user u ON e.payer_id = u.id'
        ' ORDER BY date DESC'
    )

    if error:
        flash(error)
    return render_template('auth/report.html', user=user, category=category, source=source, entries=entries)
