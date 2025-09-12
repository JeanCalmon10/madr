from http import HTTPStatus

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.core.database import get_db
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

app = FastAPI(title="MADR API")

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
    """Register a new user."""
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
            username=user.username,
            email=user.email,
            password=hashed_password,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user