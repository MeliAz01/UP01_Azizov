from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book
from ..schemas import BookCreate, BookUpdate, BookOut

router = APIRouter(prefix="/api/books", tags=["Книги"])

@router.get("/", response_model=list[BookOut])
def list_books(title: str | None = None, author: str | None = None,
               genre: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Book)
    if title:
        stmt = stmt.where(Book.title.ilike(f"%{title}%"))
    if author:
        stmt = stmt.where(Book.author.ilike(f"%{author}%"))
    if genre:
        stmt = stmt.where(Book.genre.ilike(f"%{genre}%"))
    return db.scalars(stmt.order_by(Book.title)).all()

@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(404, "Книга не найдена")
    return book

@router.post("/", response_model=BookOut, status_code=201)
def create_book(data: BookCreate, db: Session = Depends(get_db)):
    if data.available_copies > data.total_copies:
        raise HTTPException(422, "Доступно экземпляров больше, чем всего")
    book = Book(**data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, data: BookUpdate, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(404, "Книга не найдена")
    if data.available_copies > data.total_copies:
        raise HTTPException(422, "Доступно экземпляров больше, чем всего")
    for key, value in data.model_dump().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(404, "Книга не найдена")
    if db.scalar(select(Book.book_id).where(Book.book_id == book_id).where(Book.loans.any())):
        raise HTTPException(409, "Нельзя удалить книгу с историей выдач")
    db.delete(book)
    db.commit()
    return Response(status_code=204)
