from typing import Annotated, List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Query, Path,  Depends, HTTPException, Response

from app.dependencies import get_db
from app.crud.genres import get_genres, create_genre, get_genre_by_id, update_genre, delate_genre_by_id, get_books_by_genre_id
from app.schemas.genre import GenreResponse, CreateGenre, UpdataGenre, BookResponseByGenre

router  = APIRouter(tags=["genres"])

@router.get("/api/genres", response_model=List[GenreResponse])
async def get_genres_view(
    db: Annotated[Session, Depends(get_db)],
    search: Annotated[str, Query(max_length=100)] = "",
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20
):
    return get_genres(db, search, offset, limit)


@router.get("/api/genres/{id}", response_model=GenreResponse)
async def get_genres_by_id_view(
    db: Annotated[Session, Depends(get_db)],
    id: Annotated[int, Path(gt=0)]
):
    genre = get_genre_by_id(db, id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre with given ID does not exist")
    
    return genre

@router.get("/api/genres/{id}/books", status_code=200, response_model=List[BookResponseByGenre])
async def get_books_by_genre_id_view(
    db: Annotated[Session, Depends(get_db)],
    id: Annotated[int, Path(gt=0)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20
):
    return get_books_by_genre_id(db, id, offset, limit)
    


@router.post("/api/genres", response_model=GenreResponse, status_code=201)
async def post_genres_view(
    db: Annotated[Session, Depends(get_db)],
    data: CreateGenre
):
    genre = create_genre(db, data)
    if not genre:
        raise HTTPException(status_code=409, detail="This genre already exists.")
    
    return genre



@router.patch("/api/genres/{id}", status_code=200, response_model=GenreResponse)
async def path_genre_by_id_view(
    db: Annotated[Session, Depends(get_db)],
    id: Annotated[int, Path(gt=0)],
    data: UpdataGenre
):
    return update_genre(db, data, id)


@router.delete("/api/genres/{id}", status_code=204)
async def delate_genre_by_id_view(
    db: Annotated[Session, Depends(get_db)],
    id: Annotated[int, Path(gt=0)]
):
    delate_genre_by_id(db, id)

    return Response(status_code=204)