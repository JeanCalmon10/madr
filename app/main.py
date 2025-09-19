from typing import Annotated

from http import HTTPStatus

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.core.database import get_db
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.core.auth import get_current_user

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

app = FastAPI(title="MADR API")

oauth2 = OAuth2PasswordBearer(tokenUrl='token')

@app.get('/')
def home():
    """Root endpoint."""
    return {"message": "welcome to My Digital Collection of Novels"}

@app.get('/health')
def health_check(db: Session = Depends(get_db)):
    """Guarantees that the database is connected."""
    try:
        # Test connection
        db.execute(text('SELECT 1'))
        return {'status': 'Database connected successfully'}
    except Exception as e:
        return {'status': 'Database connection failed', 'error': str(e)}

@app.get('/password-test/{password}')
def password_test(password: str):
    """Test password hashing and verification."""
    hashed = hash_password(password)
    is_verified = verify_password(password, hashed)
    return {
        'original_password': password,
        'hashed_password': hashed,
        'is_verified': is_verified,
    }

@app.post('/', response_model=UserResponse, status_code=HTTPStatus.CREATED)
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

@app.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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

@app.get('/users/me', response_model=UserResponse, status_code=HTTPStatus.OK)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """Get the current authenticated user."""
    return current_user

    