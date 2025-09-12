from pydantic import BaseModel

class Token(BaseModel):
    """Validate data for returning an access token."""
    access_token: str
    token_type: str
