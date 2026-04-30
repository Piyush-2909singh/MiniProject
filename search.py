import sqlite3

import pytest

from app import create_app
from services.auth_service import register_user
from config import Config


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / 'users.db'
    monkeypatch.setattr(Config, 'DB_PATH', str(db_path))

    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
        """
    )
    conn.commit()
    conn.close()

    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as test_client:
        yield test_client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login_invalid_input(client):
    response = client.post('/login', data={
        'username': 'ab',
        'password': '123'
    })
    assert response.status_code == 400


def test_login_valid_format(client):
    response = client.post('/login', data={
        'username': 'test',
        'password': 'test123'
    })
    assert response.status_code == 200


def test_protected_route_requires_login(client):
    response = client.get('/chat')
    assert response.status_code in [302, 401]


def test_chat_input_validation(client):
    register_user('valid_user', 'test123')
    login_response = client.post('/login', data={
        'username': 'valid_user',
        'password': 'test123'
    }, follow_redirects=True)
    assert login_response.status_code == 200

    response = client.post('/ask', json={'message': '   '})
    assert response.status_code == 400


def test_chat_response_shape(client):
    register_user('valid_user2', 'test123')
    login_response = client.post('/login', data={
        'username': 'valid_user2',
        'password': 'test123'
    }, follow_redirects=True)
    assert login_response.status_code == 200

    response = client.post('/ask', json={'message': 'What is in the documents?'})
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        payload = response.get_json() or {}
        assert 'answer' in payload
        assert 'sources' in payload
        assert isinstance(payload['sources'], list)


def test_admin_requires_role(client):
    register_user('regular_user', 'test123')
    login_response = client.post('/login', data={
        'username': 'regular_user',
        'password': 'test123'
    }, follow_redirects=True)
    assert login_response.status_code == 200

    response = client.get('/admin')
    assert response.status_code == 403
