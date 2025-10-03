from fastapi import FastAPI
from .books.router import book_app
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await init_db()
    yield
    print("Shutting down...")


version = "v1"

app = FastAPI(
    title="Book Management API",
    description="API for managing a collection of books",
    version=version,
    lifespan=lifespan,
)


app.include_router(
    book_app,
    prefix=f"/api/{version}/books",
    tags=["Books"]
)
