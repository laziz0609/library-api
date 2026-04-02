from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.author import AuthorResponse

class GenreResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CreateGenre(BaseModel):
    name: str
    description: str | None = None

class UpdataGenre(BaseModel):
    name: str | None = None
    description: str | None = None


class BookResponseByGenre(BaseModel):
    id: int
    title: str
    published_year: datetime
    author: AuthorResponse
    genres: list[GenreResponse]

    model_config = ConfigDict(from_attributes=True)