from typing import List
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.genre import GenreResponse


class AuthorResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    bio: str = ""
    born_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class AuthorsResponse(BaseModel):
    limit: int = 20
    skip: int = 0
    search: str = ""
    count: int
    result: List[AuthorResponse]


class Authorcreate(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    bio: str = ""
    born_date: datetime | None = None

    @field_validator("first_name", "last_name")
    @classmethod
    def validate(cls, v: str):
        if not v.strip():
            raise ValueError("Cannot be empty or whitespace only")
        return v.strip()


class AuthorUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    bio: str = None
    born_date: datetime | None = None

    @field_validator("first_name", "last_name", "bio")
    @classmethod
    def validate(cls, v: str):
        if not v.strip():
            raise None
        return v.strip()


class AuthorBookResponse(BaseModel):
    id: int
    title: str
    published_year: int
    author: AuthorResponse
    genres: list[GenreResponse]


class AuthorBooksResponse(BaseModel):
    limit: int = 20
    skip: int = 0
    count: int
    result: List[AuthorBookResponse]
