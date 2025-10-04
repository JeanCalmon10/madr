from http import HTTPStatus

from fastapi.testclient import TestClient

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

def test_create_user(client):
    """Test creating a new user."""
    response = client.post(
        '/users/',
        json={
            'username': 'Jean',
            'email': 'jeancalmon10@gmail.com',
            'password': 'secret',
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Jean',
        'email': 'jeancalmon10@gmail.com',
        'id': 1,
    }