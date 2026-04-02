from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey

from app.database import Base



class BookGenres(Base):
    __tablename__ = 'book_genres'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"))    
    genre_id: Mapped[int] = mapped_column(Integer, ForeignKey("genres.id", ondelete="CASCADE")) 