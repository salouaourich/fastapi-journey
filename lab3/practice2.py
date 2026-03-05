from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

books = [
    {"id": 1, "title": "1984", "author": "George Orwell", "year": 1949},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925}
]


class Book(BaseModel):
    title: str
    author: str
    year: int


@app.post("/books/")
async def add_book(book: Book):

    book_id = max(b["id"] for b in books) + 1 if books else 1

    new_book = {
        "id": book_id,
        "title": book.title,
        "author": book.author,
        "year": book.year
    }

    books.append(new_book)

    return {"message": "Book added successfully", "details": new_book}