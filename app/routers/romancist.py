from fastapi import APIRouter
from fastapi import Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from typing import Annotated

from app.core.auth import get_current_user
from app.core.database import get_db

from app.schemas.romancist import RomancistResponse, RomancistCreate, RomancistUpdate, RomancistList, Message

from app.models.romancist import Romancist
from app.models.user import User

from app.utils.sanitize import sanitize_name

from http import HTTPStatus

router = APIRouter(
    prefix='/romancists',
    tags=['Romancist'],
)

@router.post('/', response_model=RomancistResponse, status_code=HTTPStatus.CREATED)
def create_romancist(
    romancist: RomancistCreate, 
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """Create a new romancist."""
    sanitized_name = sanitize_name(romancist.name) # Sanitize the romancist name

    db_romancist = db.scalar(
        select(Romancist).where(Romancist.name == sanitized_name) # Check for existing romancist with sanitized name
    )

    if db_romancist:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Romancist is already listed in MADR",
        )
    
    # Create new romancist with sanitized name
    db_romancist = Romancist(
        name=sanitized_name,
    )

    db.add(db_romancist)
    db.commit()
    db.refresh(db_romancist)

    return db_romancist

@router.get('/{romancist_id}', response_model=RomancistResponse, status_code=HTTPStatus.OK)
def read_romancist(romancist_id: int, db: Session = Depends(get_db)):
    """Get a romancist by ID."""
    db_romancist = db.scalar(
        select(Romancist).where(Romancist.id == romancist_id)
    )

    if not db_romancist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Romancist is not listed in MADR",
        )
    
    return db_romancist

@router.put('/{romancist_id}', response_model=RomancistResponse)
def update_romancist(
    romancist_id: int,
    romancist: RomancistUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """Update a romancist by ID."""
    db_romancist = db.scalar(
        select(Romancist).where(Romancist.id == romancist_id)
    )

    if not db_romancist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Romancist is not listed in MADR",
        )
    
    try:
        # Update fields if they are provided
        if romancist.name is not None:
            sanitized_name = sanitize_name(romancist.name)
            db_romancist.name = sanitized_name
    
        db.commit()
        db.refresh(db_romancist)
    
        return db_romancist
    
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Romancist is already listed in MADR",
        )

@router.delete('/{romancist_id}', response_model=Message)
def delete_romancist(
    romancist_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """Delete a romancist by ID."""
    db_romancist = db.scalar(
        select(Romancist).where(Romancist.id == romancist_id)
    )

    if not db_romancist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Romancist is not listed in MADR",
        )
    
    db.delete(db_romancist)
    db.commit()

    return {'message': 'Romancist deleted successfully'}

@router.get('/', response_model=RomancistList, status_code=HTTPStatus.OK)
def read_romancists(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    nome: str | None = None
):
    """Get a list of romancists with optional search query and conditional pagination."""
    query = select(Romancist)
    if nome:
        query = query.where(Romancist.name.ilike(f'%{nome}%'))
    
    # If a search query is provided, return all matching results.
    total = db.scalar(
        select(func.count()).select_from(query.subquery())
    )

    # Apply pagination only if there is a total results more than 20.
    if total > 20:
        query = query.offset(skip).limit(limit)
    
    db_romancists = db.scalars(query).all()
    
    return {'romancists': db_romancists}
