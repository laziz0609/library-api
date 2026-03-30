from typing import List
from datetime import date

from sqlalchemy.orm import Session

from app.models.genre import Genre
from app.models.book import Book
from app.models.book_genre import BookGenre


def get_genres(
    db: Session, search: str = "", offset: int = 0, limit: int = 20
) -> List[Genre]:
    q = db.query(Genre)

    if search != "":
        pattern = f"%{search}%"

        q = q.filter(Genre.name.ilike(pattern))

    genres = q.offset(offset).limit(limit).all()

    return genres


def create_genre(db: Session, name: str, description: str) -> Genre:
    existing_genre = db.query(Genre).filter(Genre.name == name).first()

    if existing_genre:
        raise ValueError("A genre with this name already exists")

    genre = Genre(name=name, description=description)

    db.add(genre)
    db.commit()
    db.refresh(genre)

    return genre


def get_genre_by_id(db: Session, id: int) -> Genre:
    genre = db.query(Genre).filter(Genre.id == id).first()

    if genre is None:
        raise ValueError("Genre with given ID does not exist")

    return genre


def get_genre_by_name(db: Session, name: str) -> Genre:
    genre = db.query(Genre).filter(Genre.name == name).first()

    if genre:
        raise ValueError("New name already used by another genre")

    return name


def update_genre_by_id(
    db: Session, id: int, name: str | None, description: str | None
) -> Genre:
    existing_genre = get_genre_by_id(db, id)

    if name:
        name = get_genre_by_name(db, name)
        existing_genre.name = name
    if description:
        existing_genre.description = description

    db.add(existing_genre)
    db.commit()
    db.refresh(existing_genre)

    return existing_genre


def delete_genre_by_id(db: Session, id: int) -> bool:
    existing_genre = get_genre_by_id(db, id)

    db.delete(existing_genre)
    db.commit()

    return True


def get_genre_books(
    db: Session, id: int, skip: int = 0, limit: int = 20
) -> tuple[Genre | Book]:
    genre = get_genre_by_id(db, id)

    books = (
        db.query(Book)
        .join(BookGenre)
        .filter(BookGenre.genre_id == id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return genre, books
