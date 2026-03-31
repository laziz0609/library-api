from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Book, BookGenre
from app.crud.author import get_author_by_id
from app.crud.genre import get_genre_by_id


def get_books(
    db: Session,
    search: str = "",
    author_id: int | None = None,
    genre_id: int | None = None,
    from_year: int | None = None,
    to_year: int | None = None,
    offset: int = 0,
    limit: int = 20,
) -> List[Book]:
    q = db.query(Book)

    if search != "":
        pattern = f"%{search}%"

        q = q.filter(Book.title.ilike(pattern))
    if author_id:
        q = q.filter(Book.author_id == author_id)
    if genre_id:
        q = q.join(BookGenre).filter(BookGenre.genre_id == genre_id)
    if from_year:
        q = q.filter(Book.published_year >= from_year)
    if to_year:
        q = q.filter(Book.published_year <= to_year)

    books = q.offset(offset).limit(limit).all()

    return books


def create_book(
    db: Session,
    title: str,
    author_id: int,
    genre_ids: list[int],
    description: str,
    isbn: str,
    published_year: int,
    pages: int,
) -> Book:
    author = get_author_by_id(db, author_id)
    genres = [get_genre_by_id(db, id) for id in genre_ids]

    if get_book_by_isbn(db, isbn):
        raise HTTPException(status_code=400, detail="isbn already exists")

    author = get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="author not found")

    book = Book(
        title=title,
        description=description,
        isbn=isbn,
        published_year=published_year,
        pages=pages,
        author_id=author_id,
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    if genre_ids:
        book_genres = [BookGenre(book_id=book.id, genre_id=id) for id in genre_ids]
        db.add_all(book_genres)
        db.commit()

    return book


def get_book_by_isbn(db: Session, isbn: str) -> Book | None:
    return db.query(Book).filter(Book.isbn == isbn).first()


def get_book_by_id(db: Session, id: int) -> Book | None:
    book = db.query(Book).filter(Book.id == id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="book not found")

    return book


def update_book_by_id(
    db: Session,
    id: int,
    title: str | None,
    description: str | None,
    isbn: str | None,
    published_year: int | None,
    pages: int | None,
    author_id: int | None,
    genre_ids: list[int | None] | None,
) -> Book:
    existing_book = get_book_by_id(db, id)

    if title:
        existing_book.title = title 
    if description:
        existing_book.description = description
    if isbn:
        if get_book_by_isbn(db, isbn):
            raise HTTPException(status_code=400, detail="isbn already exists")
        existing_book.isbn = isbn
    if published_year:
        existing_book.published_year = published_year
    if pages:
        existing_book.pages = pages
    if author_id:
        if get_author_by_id(db, author_id):
            existing_book.author_id = author_id
    if genre_ids == []:
        db.query(BookGenre).filter(BookGenre.book_id == id).delete()
    if genre_ids is not None:
        db.query(BookGenre).filter(BookGenre.book_id == id).delete()

        if genre_ids:
            new_relations = [
                BookGenre(book_id=id, genre_id=g_id)
                for g_id in genre_ids
            ]
            db.add_all(new_relations)
            db.commit()

    db.add(existing_book)
    db.commit()
    db.refresh(existing_book)

    return existing_book


def delete_book_by_id(db: Session, id: int) -> bool|None:
    existing_book = get_book_by_id(db, id)

    genres = existing_book.book_genres

    for genre in genres:
        db.delete(genre)

    db.delete(existing_book)
    db.commit()

    return True