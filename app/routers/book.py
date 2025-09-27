from fastapi import APIRouter
from fastapi import Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from typing import Annotated

from app.core.auth import get_current_user
from app.core.database import get_db

from app.schemas.book import BookResponse, BookCreate, BookUpdate, BookList, Message

from app.models.book import Book
from app.models.user import User
from app.models.romancist import Romancist

from http import HTTPStatus


router = APIRouter(
    prefix='/books',
    tags=['Book'],
)

@router.post('/', response_model=BookResponse, status_code=HTTPStatus.CREATED)
def create_book(
    book: BookCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """Create a new book."""
    db_book = db.scalar(
        select(Book).where(Book.title == book.title)
    )

    if db_book:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Book already exists",
        )
   
    # Check if the romancist exists
    db_romancist = db.scalar(
        select(Romancist).where(Romancist.id == book.romancist_id)
    )

    if not db_romancist:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Romancist does not exist",
        )
    
    db_book = Book(
        title=book.title,
        year=book.year,
        romancist_id=book.romancist_id,
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


@router.get('/{book_id}', response_model=BookResponse, status_code=HTTPStatus.OK)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Get a book by ID."""
    db_book = db.scalar(
        select(Book).where(Book.id == book_id)
    )

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found",
        )
    
    return db_book

@router.put('/{book_id}', response_model=BookResponse)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """Update a book by ID."""
    db_book = db.scalar(
        select(Book).where(Book.id == book_id)
    )

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found",
        )
    
    try:
        if book_update.title is not None:
            db_book.title = book_update.title
        if book_update.year is not None:
            db_book.year = book_update.year
        if book_update.romancist_id is not None:
            # Check if the romancist exists
            db_romancist = db.scalar(
                select(Romancist).where(Romancist.id == book_update.romancist_id)
            )

            if not db_romancist:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Romancist does not exist. Cannot update book with non-existent romancist.",
                )
            
            db_book.romancist_id = book_update.romancist_id

            db.commit()
            db.refresh(db_book)

            return db_book

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Book with this title already exists",
        )

@router.delete('/{book_id}', response_model=Message)
def delete_book(
    book_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """Delete a book by ID."""
    db_book = db.scalar(
        select(Book).where(Book.id == book_id)
    )

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found",
        )
    
    db.delete(db_book)
    db.commit()

    return {'message': 'Book deleted successfully'}

@router.get('/', response_model=BookList, status_code=HTTPStatus.OK)
def read_books(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    titulo: str | None = None,
    ano: int | None = None,
):
    """Get a list of books with more than one parameter with pagination."""
    query = select(Book)

    if titulo:
        query = query.where(Book.title.ilike(f'%{titulo}%'))
    
    if ano:
        query = query.where(Book.year == ano)
    
    # If a search query is provided, return all matching results.
    total = db.scalar(
        select(func.count()).select_from(query.subquery())
    )

    if total > 20:
        query = query.offset(skip).limit(limit)
    
    db_books = db.scalars(query).all()

    return {'books': db_books}
    

