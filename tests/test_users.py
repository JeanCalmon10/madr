from http import HTTPStatus

from fastapi.testclient import TestClient

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate


def test_create_user_success(client, session):
    """Test creating a new user."""
    payload = {
        'username': 'Jean',
        'email': 'jeancalmon10@gmail.com',
        'password': 'secret',
    }

    response = client.post('users/', json=payload)

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()
    assert data['username'] == payload['username']
    assert data['email'] == payload['email']
    assert isinstance(data['id'], int)

    # Check if the user is actually in the database
    user_in_db = session.query(User).filter_by(email=payload['email']).first()

    assert user_in_db is not None
    assert user_in_db.username == payload['username']

def test_create_username_conflict(client, session, user):
    """Test creating a user with existing username."""
    conflicted_payload = {
        'username': user.username,
        'email': 'newone@test.com',
        'password': 'newpassword',
    }

    response = client.post('users/', json=conflicted_payload)
    
    assert response.status_code == HTTPStatus.CONFLICT

    data = response.json()

    assert data['detail'] == 'Username already exists'

def test_create_email_conflict(client, session, user):
    """Test creating a user with existing email."""
    conflicted_payload = {
        'username': 'newone',
        'email': user.email,
        'password': 'newpassword',
    }

    response = client.post('users/', json=conflicted_payload)

    assert response.status_code == HTTPStatus.CONFLICT

    data = response.json()

    assert data['detail'] == 'Email already exists'


def test_read_user_id_success(client, user: User):
    """Test reading a user by ID."""
    response = client.get(f'users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    
    data = response.json()
    
    assert data['id'] == user.id

def test_read_user_id_not_found(client, user: User):
    """Test reading a non-existing user by ID."""
    response = client.get(f'users/{user.id + 1}')

    assert response.status_code == HTTPStatus.NOT_FOUND

    data = response.json()

    assert data['detail'] == 'User not found'


def test_users_me_success(client, token: str, user: User):
    """Test reading the current authenticated user."""
    response = client.get(
        '/users/me',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['id'] == user.id
    assert data['username'] == user.username
    assert data['email'] == user.email

def test_users_me_unathorized(client):
    """Test reading the current user without a token."""
    response = client.get('/users/me')

    assert response.status_code == HTTPStatus.UNAUTHORIZED

    data = response.json()

    data['detail'] == 'Not authenticated'


def test_update_user_success(client, token: str, user: User):
    """Test updating the current authenticated user."""
    response = client.put(
        f'users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'UpdatedName',
            'email': 'updated@test.com',
            'password': 'updatedpassword',
        }
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['id'] == user.id

def test_update_user_unathorized(client):
    """Test updating the current user without a token."""
    response = client.put(
        'users/10',
        json={
            'username': 'UpdatedName1',
            'email': 'email@email.com',
            'password': 'updatedpassword',
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

    data = response.json()

    assert data['detail'] == 'Not authenticated'


def test_delete_user_success(client, token: str, user: User):
    """Test deleting the current authenticated user."""
    response = client.delete(
        f'users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    
    data = response.json()

    assert data['message'] == 'User deleted successfully'

def test_delete_user_unauthorized(client, user: User):
    """Test deleting the current user without a token."""
    response = client.delete(f'users/{user.id}')

    assert response.status_code == HTTPStatus.UNAUTHORIZED

    data = response.json()

    assert data['detail'] == 'Not authenticated'