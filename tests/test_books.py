from http import HTTPStatus

from app.models.book import Book
from app.schemas.book import BookCreate, BookResponse, BookUpdate, BookList
from app.utils.sanitize import sanitize_name

def test_create_book(client, session, token: str, romancist):
    """Test creating a new book."""
    sanitized_title = sanitize_name('New Book Title')

    payload = {
        'title': sanitized_title,
        'year': 2025,
        'romancist_id': romancist.id
    }

    response = client.post(
        f'/books/',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data['title'] == payload['title']
    assert data['year'] == payload['year']
    assert data['romancist_id'] == payload['romancist_id']

    assert isinstance(data['id'], int)

    book_in_db = session.query(Book).filter_by(title=payload['title']).first()

    assert book_in_db is not None
    assert book_in_db.title == payload['title']

def test_create_book_conflict(client, session, token: str, book: Book):
    """Test creating a book that already exists."""
    sanitized_title = sanitize_name('Test Book')

    payload = {
        'title': sanitized_title,
        'year': 2020,
        'romancist_id': book.romancist_id
    }

    response = client.post(
        f'/books/',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT

    data = response.json()

    assert data['detail'] == 'Book is already listed in MADR'

