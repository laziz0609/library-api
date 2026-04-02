from typing import Annotated, List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Query, Depends

from app.dependencies import get_db
from app.crud.genres import get_genres
from app.schemas.genre import GenreResponse

router  = APIRouter(tags=["genres"])

@router.get("/api/genres", response_model=List[GenreResponse])
async def get_genres_view(
    db: Annotated[Session, Depends(get_db)],
    search: Annotated[str, Query(max_length=100)] = "",
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20
):
    return get_genres(db, search, offset, limit)