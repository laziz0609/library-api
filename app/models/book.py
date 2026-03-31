from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, ForeignKey

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    isbn: Mapped[str] = mapped_column(String(length=20), unique=True)
    published_year: Mapped[int] = mapped_column(Integer)
    pages: Mapped[int] = mapped_column(Integer)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))

    author: Mapped["Author"] = relationship(back_populates="books")

    def __str__(self):
        return f"{self.id}. {self.title}"
