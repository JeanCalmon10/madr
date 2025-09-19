from sqlalchemy.orm import registry

mapper_registry = registry()
Base = mapper_registry.generate_base()

from app.models.user import User
from app.models.book import Book
from app.models.romancist import Romancist