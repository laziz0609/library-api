from typing import List

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.genre import Genre
from app.models.book import Book
from app.models.book_genres import BookGenres
from app.schemas.genre import CreateGenre, UpdataGenre



def get_genres(db: Session, search: str, offset: int, limit: int) -> List[Genre]:
    if search == "":
        return db.query(Genre).offset(offset).limit(limit)
    
    pattern = f"%{search}%"
    return db.query(Genre).filter(Genre.name.ilike(pattern)).offset(offset).limit(limit)

def get_genre_by_id(db: Session, id: int) -> Genre | None:
    genre = db.query(Genre).filter_by(id=id).first()
    
    return genre

def get_books_by_genre_id(db: Session, id: int, offset: int, limit: int) -> List[Book]:
    genre = db.query(Genre).filter_by(id=id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre with given ID does not exist")
    
    return genre.books



def create_genre(db: Session, data: CreateGenre) -> Genre | None:
    cheker_genre_name = db.query(Genre).filter(func.lower(Genre.name) == data.name.lower()).first()
    if cheker_genre_name:
        return None
    
    genre = Genre(
        name = data.name,
        description = data.description
    )
    db.add(genre)
    db.commit()
    db.refresh(genre)

    return genre


def update_genre(db: Session, data: UpdataGenre, id: int) -> Genre:
    genre = db.query(Genre).filter_by(id=id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre with given ID does not exist")
    
    if data.name:
        cheker_name = db.query(Genre).filter(func.lower(Genre.name) == data.name.lower()).first()
        if cheker_name:
            raise HTTPException(status_code=400, detail="New name already used by another genre")
        
    genre.name = data.name if data.name else genre.name
    genre.description = data.description if data.description else genre.description

    db.commit()
    db.refresh(genre)

    return genre

def delate_genre_by_id(db: Session, id: int) -> None:
    genre = db.query(Genre).filter_by(id=id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre with given ID does not exist")
    
    db.delete(genre)
    db.commit()
