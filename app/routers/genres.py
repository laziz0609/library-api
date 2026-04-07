from typing import Annotated

from fastapi import APIRouter, Query, Path, HTTPException, Body, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.genre import (
    GenresResponse,
    GenreCreate,
    GenreResponse,
    GenreUpdate,
    GenreBookItemResponse,
    GenreBookListResponse,
)
from app.schemas.author import AuthorResponse
from app.crud.genre import (
    get_genres,
    create_genre,
    get_genre_by_id,
    update_genre_by_id,
    delete_genre_by_id,
    get_genre_books,
)
from app.security import verify_token

router = APIRouter(tags=["genres"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.get("/api/genres", response_model=GenresResponse, status_code=200)
async def get_genres_view(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
    search: Annotated[str, Query()] = "",
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="invalid token.")

    genres = get_genres(db, search, skip, limit)

    response = GenresResponse(
        limit=limit, skip=skip, search=search, count=len(genres), result=genres
    )

    return response


@router.post("/api/genres", status_code=201)
async def create_genre_view(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
    data: Annotated[GenreCreate, Body],
):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="invalid token.")

    genre = create_genre(db=db, name=data.name, description=data.description)

    response = GenreResponse(
        id=genre.id, name=genre.name, description=genre.description
    )

    return response


@router.get("/api/genres/{id}")
async def get_genre_by_id_view(
    id: Annotated[int, Path(gt=0)],
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="invalid token.")

    genre = get_genre_by_id(db=db, id=id)

    response = GenreResponse(
        id=genre.id, name=genre.name, description=genre.description
    )

    return response


@router.patch("/api/genres/{id}")
async def update_genre_by_id_view(
    id: Annotated[int, Path(gt=0)],
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
    data: Annotated[GenreUpdate | None, Body] = None,
):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="invalid token.")

    genre = update_genre_by_id(
        db=db, id=id, name=data.name, description=data.description
    )

    response = GenreResponse(id=id, name=genre.name, description=genre.description)

    return response


@router.delete("/api/genres/{id}", status_code=204)
async def delete_genre_by_id_view(
    id: Annotated[int, Path(gt=0)],
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="invalid token.")

    genre = delete_genre_by_id(db=db, id=id)


@router.get("/genres/{id}/books")
async def get_genre_books_view(
    id: Annotated[int, Path(gt=0)],
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="invalid token.")

    genres, books = get_genre_books(db=db, id=id, skip=skip, limit=limit)

    book_responses = []
    for book in books:
        author = AuthorResponse(
            id=book.author.id,
            first_name=book.author.first_name,
            last_name=book.author.last_name,
            bio=book.author.bio,
            born_date=book.author.born_date,
        )

        genres = [
            GenreResponse(
                id=bg.genre.id, name=bg.genre.name, description=bg.genre.description
            )
            for bg in book.book_genres
        ]

        book_response = GenreBookItemResponse(
            id=book.id,
            title=book.title,
            published_year=book.published_year,
            author=author,
            genres=genres,
        )
        book_responses.append(book_response)

    return GenreBookListResponse(
        limit=limit, skip=skip, count=len(books), result=book_responses
    )
