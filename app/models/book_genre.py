from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class BookGenre(Base):
    __tablename__ = "book_genres"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), primary_key=True)

    book: Mapped["Book"] = relationship("Book", back_populates="book_genres")
    genre: Mapped["Genre"] = relationship("Genre", back_populates="book_genres")
