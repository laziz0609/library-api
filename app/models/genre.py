from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  Text, Integer, VARCHAR

from app.database import Base


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(100), unique=True, nullable=False)
    description: Mapped[str] =  mapped_column(Text)   

    books: Mapped[list["Book"]] = relationship(back_populates="genres", secondary="book_genres")
