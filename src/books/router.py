from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from .book_data import Books
from .schemas import Book , UpdateBook

book_app = APIRouter()



@book_app.get("/", response_model=List[Book])
async def get_books():
    return Books

@book_app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()
    Books.append(new_book)
    return new_book

@book_app.get("/{book_id}")
async def get_book(book_id: int) -> Book:
    for book in Books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@book_app.patch("/{book_id}",status_code=status.HTTP_202_ACCEPTED)
async def update_book(book_id: int, book: UpdateBook) -> Book:
    for i , b in enumerate(Books):
        if b["id"] == book_id:
            Books[i].update(book.model_dump())
            return Books[i]
    raise HTTPException(status_code=404, detail="Book not found")


@book_app.delete("/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for i , b in enumerate(Books):
        if b["id"] == book_id:
            Books.pop(i)
            return {}
    raise HTTPException(status_code=404, detail="Book not found")