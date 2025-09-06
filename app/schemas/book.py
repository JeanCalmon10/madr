from pydantic import BaseModel, ConfigDict

class BookCreate(BaseModel):
    """Validate data for creating a new book."""
    title: str
    year: int
    romancist_id: int

class BookResponse(BaseModel):
    """Validate data for returning book information."""
    id: int
    title: str
    year: int
    romancist_id: int

    model_config = ConfigDict(from_attributes=True) # Allow ORM mode


class BookUpdate(BaseModel):
    """Validate data for updating book information."""
    title: str | None = None
    year: int | None = None
    romancist_id: int | None = None
   

