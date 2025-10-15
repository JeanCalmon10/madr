from http import HTTPStatus

from app.models.romancist import Romancist
from app.schemas.romancist import RomancistCreate, RomancistResponse, RomancistUpdate, RomancistList
from app.utils.sanitize import sanitize_name

from pprint import pprint

def test_create_romancist(client, session, token: str):
    """Test creating a new romancist."""
    sanitized_name = sanitize_name('New Romancist')

    payload = {
        'name': sanitized_name,
    }

    response = client.post(
        '/romancists/', 
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data['name'] == payload['name']
    assert isinstance(data['id'], int)

    romancist_in_db = session.query(Romancist).filter_by(name=payload['name']).first()

    assert romancist_in_db is not None
    assert romancist_in_db.name == payload['name']


def test_create_romancist_conflict(client, session, token: str, romancist: Romancist):
    """Test creating a romancist that already exists."""
    sanitized_name = sanitize_name('Test Romancist')

    payload = {
        'name': sanitized_name,
    }

    response = client.post(
        '/romancists/',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT

    data = response.json()

    assert data['detail'] == 'Romancist is already listed in MADR'

def test_read_romancist_success(client, romancist: Romancist):
    """Test reading a romancist by ID."""
    response = client.get(f'/romancists/{romancist.id}')

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['id'] == romancist.id

def test_read_romancist_not_found(client, romancist: Romancist):
    """Test reading a non-existent romancist by ID."""
    response = client.get(f'/romancists/{romancist.id + 1}')

    assert response.status_code == HTTPStatus.NOT_FOUND

    data = response.json()

    assert data['detail'] == 'Romancist is not listed in MADR'

def test_read_romancists_success(client, romancists: RomancistList):
    """Test reading all romancists."""
    response = client.get('/romancists/')

    assert response.status_code == HTTPStatus.OK

    data = response.json()
    pprint(f'data: {data}')
    
    assert data['romancists'] is not None

def test_read_romancists_pagination(client, romancists: RomancistList):
    """Test reading romancists with pagination."""
    response = client.get('/romancists/?skip=1&limit=1')

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    pprint(f'data: {data}')
    assert len(data['romancists']) == 3


def test_read_romancists_empty(client):
    """Test reading romancists when none exist."""
    response = client.get('/romancists/')

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['romancists'] == []

def test_update_romancist_success(client, session, token: str, romancist: Romancist):
    """Test updating a romancist by ID."""
    sanitized_name = sanitize_name('Updated Romancist')

    response = client.put(
        f'/romancists/{romancist.id}',
        json={'name': sanitized_name},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['id'] == romancist.id

def test_update_romancist_not_found(client, token: str, romancist: Romancist):
    """Test updating a non-existent romancist by ID."""
    sanitized_name = sanitize_name('Updated Romancist')

    response = client.put(
        f'/romancists/{romancist.id + 1}',
        json={'name': sanitized_name},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    data = response.json()

    assert data['detail'] == 'Romancist is not listed in MADR'

def test_update_romancist_conflict(client, session, token: str, romancists: RomancistList):
    """Test updating a romancist to a name that already exists."""
    romancist_update = romancists[0]

    existing_romancist = romancists[1]

    response = client.put(
        f'/romancists/{romancist_update.id}',
        json={'name': existing_romancist.name},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT

    data = response.json()

    assert data['detail'] == 'Romancist is already listed in MADR'

def test_delete_romancist_success(client, session, token: str, romancist: Romancist):
    """Test deleting a romancist by ID."""
    response = client.delete(
        f'/romancists/{romancist.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['message'] == 'Romancist deleted successfully'

def test_delete_romancist_not_found(client, romancist: Romancist, token: str):
    """Test deleting a non-existent romancist by ID."""
    response = client.delete(
        f'/romancists/{romancist.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json()
    assert data['detail'] == 'Romancist is not listed in MADR'

