from fastapi import FastAPI

from app.database import engine, Base
from app.models import *
from app.routers.authors import router as authors_router
from app.routers.books import router as books_router
from app.routers.genres import router as genre_router


Base.metadata.create_all(engine)

app = FastAPI(title="Library API")

app.include_router(authors_router)
app.include_router(books_router)
app.include_router(genre_router)
