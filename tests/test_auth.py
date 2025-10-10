from http import HTTPStatus

from fastapi.testclient import TestClient

from app.models.user import User

def login_success(client, email: str, password: str) -> str:
    """Login a user and return the JWT token."""
    payload = {
        'username': email,
        'password': password,
    }

    response = client.post('/auth/token', data=payload)

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert 'access_token' in data
    assert data['token_type'] == 'bearer'

    return data['access_token']


def test_invalid_credentials(client):
    """Test login with invalid credentials."""
    email = 'wrong@email.com'
    password = 'wrongpassword'

    payload = {
        'username': email,
        'password': password,
    }

    response = client.post('/auth/token', data=payload)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    
    data = response.json()

    assert data['detail'] == 'Invalid email or password'


def test_refresh_token_success(client, user, token: str):
    """Test refreshing a JWT token."""
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'
    