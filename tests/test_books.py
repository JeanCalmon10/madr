from http import HTTPStatus

from app.models.book import Book
from app.schemas.book import BookCreate, BookResponse, BookUpdate, BookList
from app.utils.sanitize import sanitize_name

from pprint import pprint

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

def test_create_book_bad_request(client, session, token: str):
    """Test creating a book with a non-existent romancist."""
    sanitized_title = sanitize_name('Another Book Title')

    payload = {
        'title': sanitized_title,
        'year': 2023,
        'romancist_id': 9999
    }

    response = client.post(
        f'/books/',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST

    data = response.json()

    assert data['detail'] == 'Romancis is not listed in MADR. Cannot create book with non-existent romancist.'

def test_read_book_success(client, book: Book):
    """Test reading a book by ID."""
    response = client.get(f'/books/{book.id}')

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['id'] == book.id

def test_read_book_not_found(client, book: Book):
    """Test reading a non-existent book by ID."""
    response = client.get(f'/books/{book.id + 1}')

    assert response.status_code == HTTPStatus.NOT_FOUND

    data = response.json()

    assert data['detail'] == 'Book is not listed in MADR'

def test_read_books_success(client, book: Book):
    """Test reading all books."""
    response = client.get('/books/')

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    pprint(f'data: {data}')

    assert data['books'] is not None

def test_read_books_pagination(client, book: Book):
    """Test reading books with pagination."""
    response = client.get('/books/?skip=0&limit=1')

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    pprint(f'data: {data} and size: {len(data["books"])}')

    assert len(data['books']) == 1

def test_read_books_empty(client):
    """Test reading books when none exist."""
    response = client.get('/books/')

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['books'] == []

def test_update_book_success(client, session, token: str, book: Book, romancist):
    """Test updating a book by ID."""
    sanitized_title = sanitize_name('Updated Book Title')

    response = client.put(
        f'/books/{book.id}',
        json={
            'title': sanitized_title,
            'year': 2025,
            'romancist_id': romancist.id,
        },

        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    pprint(f'data: {data}')

    assert data['title'] == sanitized_title
    assert data['year'] == 2025
    assert data['romancist_id'] == romancist.id

def test_update_book_not_found(client, token: str, book: Book, romancist):
    """Test updating a non-existent book by ID."""
    sanitizided_title = sanitize_name('Updated Book Title')

    response = client.put(
        f'/books/{book.id + 1}',
        json={
            'title': sanitizided_title,
            'year': 2025,
            'romancist_id': romancist.id
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json()['detail'] == 'Book is not listed in MADR'

def test_update_book_conflict(client, session, token: str, book: Book, romancist):
    """Test updating a book to a title that already exists."""

    # Ensure the book is in the session
    book = session.merge(book)
    
    # Create another book to cause a conflict
    other_book = Book(
        title=sanitize_name('Another Book'),
        year=2026,
        romancist_id=romancist.id
    )

    session.add(other_book) # Add the new book to the session
    session.commit() # Commit to save it to the database

    # Attempt to update the first book to have the same title as the second book
    response = client.put(
        f'/books/{other_book.id}',
        json={
            'title': book.title,
            'year': 2025,
            'romancist_id': romancist.id
        },

        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'Book is already listed in MADR'

def test_update_book_bad_request(client, session, token: str, book: Book, romancist):
    """Test updating a book with a non-existent romancist."""
    sanitized_title = sanitize_name('Updated Book')

    response = client.put(
        f'/books/{book.id}',
        json={
            'title': sanitized_title,
            'year': 2025,
            'romancist_id': romancist.id + 10
        },

        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    
    data = response.json()

    assert data['detail'] == 'Romancist does not exist. Cannot update book with non-existent romancist.'

def test_delete_book_success(client, session, token: str, book: Book):
    """Test deleting a book by ID."""
    response = client.delete(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == 'Book deleted successfully'

def test_delete_book_not_found(client, token: str, book: Book):
    """Test deleting a non-existent book by ID."""
    response = client.delete(
        f'/books/{book.id + 10}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Book is not listed in MADR'

def test_delete_book_unauthorized(client, book: Book):
    """Test deleting a book without authentication."""
    response = client.delete(f'/books/{book.id}')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Not authenticated'