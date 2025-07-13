import pytest
from bbem.db import get_db


def test_index(client, auth):
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Regisiter' in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2025-07-10' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize('path', (
                         '/create',
                         '/1/update',
                         '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == '/auth/login'


#def test_payer_required(app, client, auth):
#    with app.app_context():
#        db = get_db()
#        db.execute('UPDATE entry SET payer_id = 2 WHERE id = 1')
#        db.commit()

#    auth.login()
#    assert client.post('/1/update').status_code == 403
#    assert client.post('/1/delete').status_code == 403
#    assert b'href="/1/update"' not in client.get('/').data

@pytest.mark.parametrize('path', (
                         '/2/update',
                         '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'payee': 'created', 'category': ''})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM entries').fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'payee': 'updated', 'category': ''})

    with app.app_context():
        db = get_db()
        entry = db.execute('SELECT * FROM entries WHERE id = 1').fetchone()
        assert entry['payee'] == 'updated'


@pytest.mark.parametrize('path', (
                         '/create',
                         '/1/update',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'payee': '', 'category': ''})
    assert b'Payee is required.' in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == '/'

    with app.app_context():
        db = get_db()
        entry = db.execute('SELECT * FROM entries WHERE id = 1').fetchone()
        assert entry is None




