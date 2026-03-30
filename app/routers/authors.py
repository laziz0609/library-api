from typing import Annotated

from fastapi import APIRouter, Query, Path, HTTPException, Body, status

from app.dependencies import get_db
from app.crud.author import (
    get_authors,
    create_author,
    get_author_by_id,
    update_author_by_id,
    delete_author_by_id,
    get_author_books,
)
from app.schemas.author import (
    AuthorResponse,
    AuthorsResponse,
    Authorcreate,
    AuthorUpdate,
    AuthorBookResponse,
    AuthorBooksResponse,
)
from app.schemas.genre import GenreResponse

router = APIRouter(tags=["authors"])


@router.get("/api/authors", response_model=AuthorsResponse, status_code=200)
async def get_authors_view(
    search: Annotated[str, Query()] = "",
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
):
    db = next(get_db())

    authors = get_authors(db, search, skip, limit)

    response = AuthorsResponse(
        limit=limit, skip=skip, search=search, count=len(authors), result=authors
    )

    return response


@router.post("/api/authors", status_code=201)
async def create_author_view(data: Annotated[Authorcreate, Body]):
    db = next(get_db())

    author = create_author(
        db=db,
        first_name=data.first_name,
        last_name=data.last_name,
        bio=data.bio,
        born_date=data.born_date,
    )

    response = AuthorResponse(
        id=author.id,
        first_name=author.first_name,
        last_name=author.last_name,
        bio=author.bio,
        born_date=author.born_date,
    )

    return response


@router.get("/api/authors/{id}")
async def get_author_by_id_view(id: Annotated[int, Path(gt=0)]):
    db = next(get_db())

    try:
        author = get_author_by_id(db=db, id=id)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

    response = AuthorResponse(
        id=author.id,
        first_name=author.first_name,
        last_name=author.last_name,
        bio=author.bio,
        born_date=author.born_date,
    )

    return response


@router.patch("/api/authors/{id}")
async def update_author_by_id_view(
    id: Annotated[int, Path(gt=0)], data: Annotated[AuthorUpdate | None, Body] = None
):
    db = next(get_db())

    try:
        author = update_author_by_id(
            db=db,
            id=id,
            first_name=data.first_name,
            last_name=data.last_name,
            bio=data.bio,
            born_date=data.born_date,
        )
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

    response = AuthorResponse(
        id=author.id,
        first_name=author.first_name,
        last_name=author.last_name,
        bio=author.bio,
        born_date=author.born_date,
    )

    return response


@router.delete("/api/authors/{id}")
async def delete_author_by_id_view(id: Annotated[int, Path(gt=0)]):
    db = next(get_db())

    try:
        author = delete_author_by_id(db=db, id=id)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

    return status.HTTP_204_NO_CONTENT


@router.get("/api/authors/{id}/books")
async def get_author_books_view(
    id: Annotated[int, Path(gt=0)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
):
    db = next(get_db())

    try:
        author, books = get_author_books(db=db, id=id, skip=skip, limit=limit)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

    author = AuthorResponse(
        id=author.id,
        first_name=author.first_name,
        last_name=author.last_name,
        bio=author.bio,
        born_date=author.born_date,
    )

    book_responses = []
    for book in books:
        genres = [
            GenreResponse(id=g.id, name=g.name, description=g.description)
            for g in book.genres
        ]

        book_response = AuthorBookResponse(
            id=book.id,
            title=book.title,
            published_year=book.published_year,
            author=author,
            genres=genres,
        )
        book_responses.append(book_response)

    return AuthorBooksResponse(
        limit=limit, skip=skip, count=len(books), result=book_responses
    )
