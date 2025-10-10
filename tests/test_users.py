from http import HTTPStatus

from fastapi.testclient import TestClient

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate


def test_create_user(client, session):
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

def test_create_user_conflict(client, session, user):
    pass