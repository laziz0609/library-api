from typing import List

from sqlalchemy.orm import Session

from app.models.author import Author
from app.models.book import Book


def get_books_by_auhtor(
    db: Session, author: Author, skip: int = 0, limit: int = 20
) -> List[Book]:
    books = (
        db.query(Book).filter_by(author_id=author.id).offset(skip).limit(limit).all()
    )

    return books
