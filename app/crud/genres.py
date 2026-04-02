from typing import List

from sqlalchemy.orm import Session

from app.models.genre import Genre



def get_genres(db: Session, search: str, offset: int, limit: int) -> List[Genre]:
    if search == "":
        return db.query(Genre).offset(offset).limit(limit)
    
    pattern = f"%{search}%"
    return db.query(Genre).filter(Genre.name.ilike(pattern)).offset(offset).limit(limit)