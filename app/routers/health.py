from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.core.database import get_db

router = APIRouter(
    prefix='/health',
    tags=['Health'],
)

@router.get('/')
def health_check(db: Session = Depends(get_db)):
    """Guarantees that the database is connected."""
    try:
        # Test connection
        db.execute(text('SELECT 1'))
        return {'status': 'Database connected successfully'}
    except Exception as e:
        return {'status': 'Database connection failed', 'error': str(e)}