from fastapi import APIRouter, Depends, HTTPException

from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.core.security import hash_password
from app.core.auth import get_current_user

from app.models.user import User

from app.schemas.user import UserCreate, UserResponse, UserUpdate, Message

from typing import List
from typing import Annotated


router = APIRouter(
    prefix='/users',
    tags=['Users'],
)

@router.post('/', response_model=UserResponse, status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    db_user = db.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        ) 
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username already exists",
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email already exists",
            )
        
    hashed_password = hash_password(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        password_hash=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get('/me', response_model=UserResponse, status_code=HTTPStatus.OK)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """Get the current authenticated user."""
    return current_user

@router.get('/{user_id}', response_model=UserResponse, status_code=HTTPStatus.OK)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID."""
    db_user = db.scalar(
        select(User).where(User.id == user_id)
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )
    
    return db_user

@router.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int, 
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Delete a user by ID."""
    db_user = db.scalar(
        select(User).where(User.id == user_id)
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )
    
    if db_user.id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Not authorized to delete this user",
        )
    
    db.delete(db_user)
    db.commit()

    return {'message': 'User deleted successfully'}

@router.put('/{user_id}', response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """Update a user's information."""
    db_user = db.scalar(
        select(User).where(User.id == user_id)
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )

    if current_user.id != db_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Not authorized to update this user",
        )
    
    try:
        if user_update.username is not None:
            db_user.username = user_update.username
        if user_update.email is not None:
            db_user.email = user_update.email
        if user_update.password is not None:
            db_user.password_hash = hash_password(user_update.password)

        db.commit()
        db.refresh(db_user)

        return db_user
    
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Username or email already exists",
        )