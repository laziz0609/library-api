from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text

from app.database import Base


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    book_genres: Mapped[list["BookGenre"]] = relationship(
        "BookGenre", back_populates="genre"
    )
