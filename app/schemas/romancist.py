from pydantic import BaseModel, ConfigDict

class RomancistCreate(BaseModel):
    """Validate data for creating a new romancist."""
    name: str

class RomancistResponse(BaseModel):
    """Validate data for returning romancist information."""
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class RomancistUpdate(BaseModel):
    """Validate data for updating romancist information."""
    name: str | None = None   
