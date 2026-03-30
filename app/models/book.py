from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, SmallInteger, Integer, ForeignKey

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    isbn: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    published_year: Mapped[int] = mapped_column(SmallInteger, nullable=True)
    pages: Mapped[int] = mapped_column(Integer, nullable=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id", ondelete="CASCADE"), nullable=False
    )

    author: Mapped["Author"] = relationship("Author", back_populates="books")
    book_genres: Mapped[list["BookGenre"]] = relationship(
        "BookGenre", back_populates="book"
    )
