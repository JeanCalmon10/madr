from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship, registry

from app.models.base import Base

# Ignore circular import for type checking
if TYPE_CHECKING:
    from app.models.romancist import Romancist

class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    romancist_id: Mapped[int] = mapped_column(ForeignKey('romancists.id'))
    romancist: Mapped["Romancist"] = relationship("Romancist", back_populates='books')