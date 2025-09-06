from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    """Validate data for creating a new user."""
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Validate data for returning user information."""
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True) # Allow ORM mode

class UserUpdate(BaseModel):
    """Validate data for updating user information."""
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None

