from typing import List, Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.author import AuthorResponse
from app.schemas.genre import GenreResponse


class BookItemResponse(BaseModel):
    id: int
    title: str
    published_year: int | None
    author: AuthorResponse
    genres: List[GenreResponse]

    model_config = ConfigDict(from_attributes=True)


class BookListResponse(BaseModel):
    limit: int
    skip: int
    count: int
    result: List[BookItemResponse]


class CreateBook(BaseModel):
    title: str = Field(min_length=1)
    author_id: int = Field(gt=0)
    genre_ids: list[int] = []
    description: str | None = None
    isbn: str | None = None
    published_year: int | None = Field(ge=1000, le=2100)
    pages: int | None = Field(gt=0)

    @field_validator("title", "isbn")
    @classmethod
    def validate(cls, v: str):
        if not v.strip():
            raise ValueError("Cannot be empty or whitespace only")
        return v.strip()
    

class UpdateBook(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = None
    isbn: str | None = None
    published_year: int | None = Field(default=None, ge=1000, le=2100)
    pages: int | None = Field(default=None, gt=0)
    author_id: int | None = Field(default=None, gt=0)
    genre_ids: list[Annotated[int, Field(gt=0)]] | None = None

    @field_validator("title", "isbn")
    @classmethod
    def validate(cls, v: str):
        if not v.strip():
            return None
        return v.strip()
