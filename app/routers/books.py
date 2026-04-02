from typing import Annotated, List

from fastapi import APIRouter, Query, Path, HTTPException, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.crud.author import get_author
from app.crud.book import get_books_by_auhtor
from app.schemas.book import BookResponse


router = APIRouter(tags=["books"])


@router.get(
    "/api/authors/{id}/books", response_model=List[BookResponse], status_code=200
)
async def get_authors_view(
    id: Annotated[int, Path(ge=1)],
    db: Annotated[Session, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
):
    author = get_author(db, id)
    if author is None:
        raise HTTPException(status_code=404, detail="author not found.")

    return get_books_by_auhtor(db, author, skip, limit)
