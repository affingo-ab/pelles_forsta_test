import pytest
from pelles_app.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Logga in' in response.data

def test_successful_login(client):
    response = client.post('/', data={
        'username': 'Pelle',
        'password': 'Pelle123!'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Valkommen Pelle' in response.data or b'Dashboard' in response.data
