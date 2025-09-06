from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship, registry

from app.models.base import mapper_registry, Base

# Ignore circular import for type checking
if TYPE_CHECKING:
    from app.models.book import Book


@mapper_registry.mapped
class Romancist(Base):
    __tablename__ = 'romancists'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # One romancist can have many books
    books: Mapped[list["Book"]] = relationship("Book", back_populates='romancist', cascade="all, delete-orphan")