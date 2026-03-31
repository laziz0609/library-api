from pydantic import BaseModel, ConfigDict

from app.schemas.author import AuthorResponse


class BookResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    isbn: str | None = None
    published_year: int | None = None
    pages: int | None = None
    author: AuthorResponse

    model_config = ConfigDict(from_attributes=True)
