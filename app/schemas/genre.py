from typing import List
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class GenreCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None

    @field_validator("name")
    @classmethod
    def validate(cls, value: str):
        if not value.strip():
            raise ValueError("Cannot be empty or whitespace only")
        return value.strip()


class GenreResponse(BaseModel):
    id: int = Field(gt=0)
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class GenresResponse(BaseModel):
    limit: int = 20
    skip: int = 0
    search: str = ""
    count: int
    result: List[GenreResponse]


class GenreUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

    @field_validator("name", "description")
    @classmethod
    def validate(cls, value: str):
        if not value.strip():
            return None
        return value.strip()


class AuthorResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    bio: str = ""
    born_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class GenreBookItemResponse(BaseModel):
    id: int
    title: str
    published_year: int | None
    author: AuthorResponse
    genres: List[GenreResponse]


class GenreBookListResponse(BaseModel):
    limit: int
    skip: int
    count: int
    result: List[GenreBookItemResponse]
