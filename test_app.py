import pytest
from app import app, init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        init_db()
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b'Server is up and running' in response.data

def test_add_todo(client):
    response = client.post('/add', data={'task': 'Test Task'}, follow_redirects=True)
    assert response.status_code == 200

def test_add_empty_todo(client):
    response = client.post('/add', data={'task': ''}, follow_redirects=True)
    assert response.status_code == 200
