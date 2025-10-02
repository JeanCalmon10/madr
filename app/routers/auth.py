from fastapi import APIRouter, Depends, HTTPException

from http import HTTPStatus

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.core.database import get_db    
from app.core.security import verify_password
from app.core.jwt import create_access_token

from app.models.user import User

from app.schemas.token import Token

from app.core.auth import get_current_user

router = APIRouter(
    prefix='/auth',
    tags=['Authentication'],
)

@router.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = db.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid email or password",
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
    token = create_access_token(data={'sub': str(user.id)})

    return {
        'access_token': token,
        'token_type': 'bearer',
    }

@router.post('/refresh_token', response_model=Token)
async def refresh_token(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Refresh JWT token for the current user."""
    new_access_token = create_access_token(data={'sub': str(current_user.id)})

    return {
        'access_token': new_access_token,
        'token_type': 'bearer',
    }