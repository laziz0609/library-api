from typing import Annotated

from fastapi import APIRouter, Query, Path, Body

from app.dependencies import get_db
from app.crud.book import get_books, create_book, get_book_by_id, update_book_by_id, delete_book_by_id
from app.schemas.book import BookListResponse, BookItemResponse, CreateBook, UpdateBook
from app.schemas.genre import GenreResponse
from app.schemas.author import AuthorResponse

router = APIRouter(tags=["books"])


@router.get("/api/books", response_model=BookListResponse, status_code=200)
async def get_books_view(
    search: Annotated[str, Query()] = "",
    author_id: Annotated[int | None, Query()] = None,
    genre_id: Annotated[int | None, Query()] = None,
    year_from: Annotated[int | None, Query()] = None,
    year_to: Annotated[int | None, Query()] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
):
    db = next(get_db())

    books = get_books(
        db=db,
        search=search,
        author_id=author_id,
        genre_id=genre_id,
        from_year=year_from,
        to_year=year_to,
        offset=skip,
        limit=limit,
    )

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

        book_response = BookItemResponse(
            id=book.id,
            title=book.title,
            published_year=book.published_year,
            author=author,
            genres=genres,
        )
        book_responses.append(book_response)

    return BookListResponse(
        limit=limit, skip=skip, count=len(books), result=book_responses
    )


@router.post("/api/books", response_model=BookItemResponse, status_code=200)
async def create_book_view(data: Annotated[CreateBook, Body]):
    db = next(get_db())

    book = create_book(
        db=db,
        title=data.title,
        author_id=data.author_id,
        genre_ids=data.genre_ids,
        description=data.description,
        isbn=data.isbn,
        published_year=data.published_year,
        pages=data.pages,
    )

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

    book_response = BookItemResponse(
        id=book.id,
        title=book.title,
        published_year=book.published_year,
        author=author,
        genres=genres,
    )

    return book_response


@router.get("/api/books/{id}")
async def get_genre_by_id_view(id: Annotated[int, Path(gt=0)]):
    db = next(get_db())

    book = get_book_by_id(db, id)

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

    book_response = BookItemResponse(
        id=book.id,
        title=book.title,
        published_year=book.published_year,
        author=author,
        genres=genres,
    )

    return book_response

@router.patch("/api/books/{id}")
async def update_book_by_id_view(
    id: Annotated[int, Path(gt=0)], data: Annotated[UpdateBook, Body] = None
):
    db = next(get_db())

    book = update_book_by_id(db=db, id=id, title=data.title, description=data.description, isbn=data.isbn, published_year=data.published_year, pages=data.pages, author_id=data.author_id, genre_ids=data.genre_ids)

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

    book_response = BookItemResponse(
        id=book.id,
        title=book.title,
        published_year=book.published_year,
        author=author,
        genres=genres,
    )

    return book_response


@router.delete("/api/books/{id}", status_code=204)
async def delete_book_by_id_view(id: Annotated[int, Path(gt=0)]):

    db = next(get_db())
    delete_book_by_id(db, id)
