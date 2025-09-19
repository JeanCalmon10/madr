from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    """Validate data for returning an access token."""
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    """Validate data for login request."""
    email: EmailStr
    password: str

