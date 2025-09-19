import bcrypt
from fastapi import Depends, HTTPException, status

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a stored password against one provided by user."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


