from typing import List
from datetime import date

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.author import Author
from app.models.book import Book


def get_authors(
    db: Session, search: str = "", offset: int = 0, limit: int = 20
) -> List[Author]:
    q = db.query(Author)

    if search != "":
        pattern = f"%{search}%"

        q = q.filter(
            or_(
                Author.first_name.ilike(pattern),
                Author.last_name.ilike(pattern),
            )
        )

    authors = q.offset(offset).limit(limit).all()

    return authors


def create_author(
    db: Session,
    first_name: str,
    last_name: str,
    bio: str = None,
    born_date: date = None,
) -> Author:
    author = Author(
        first_name=first_name, last_name=last_name, bio=bio, born_date=born_date
    )

    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_author_by_id(db: Session, id: int) -> Author:
    author = db.query(Author).filter(Author.id == id).first()

    if author is None:
        raise ValueError("Author with given ID does not exist")

    return author


def update_author_by_id(
    db: Session,
    id: int,
    first_name: str | None,
    last_name: str | None,
    bio: str | None,
    born_date: date | None,
) -> Author:
    author = get_author_by_id(db=db, id=id)

    if first_name:
        author.first_name = first_name
    if last_name:
        author.last_name = last_name
    if bio:
        author.bio = bio
    if born_date:
        author.born_date = born_date

    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def delete_author_by_id(db: Session, id: int) -> True:
    author = get_author_by_id(db, id)

    db.delete(author)
    db.commit()

    return True


def get_author_books(
    db: Session, id: int, skip: int = 0, limit: int = 20
) -> tuple[Author, Book]:
    author = get_author_by_id(db, id)

    books = db.query(Book).filter(Book.author_id == id).offset(skip).limit(limit).all()

    return author, books
